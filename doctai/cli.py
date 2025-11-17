"""
Command-line interface for documentation tester.
"""

import argparse
import sys
import os
import json
from doctai.ai_client import AIClient
from doctai.orchestrator import DocumentationTester
from doctai.config import ConfigLoader


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="AI-powered documentation tester - Automatically test documentation by generating and running test scripts",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Test documentation from a local file
  doctai --docs README.md --api-key $OPENAI_API_KEY
  
  # Test documentation from a URL
  doctai --docs https://example.com/setup.md --api-key $ANTHROPIC_API_KEY --provider anthropic
  
  # Test multiple documentation sources
  doctai --docs README.md docs/setup.md --api-key $API_KEY
  
  # Use custom AI endpoint
  doctai --docs README.md --api-key $API_KEY --api-url https://custom-ai.com/v1/chat --provider custom --model gpt-4
  
  # Save results to JSON file
  doctai --docs README.md --api-key $API_KEY --output results.json
  
Environment variables:
  DOCTAI_API_KEY     API key for AI provider
  DOCTAI_API_URL     Custom API URL
  DOCTAI_PROVIDER    AI provider (openai, anthropic, custom)
  DOCTAI_MODEL       Model name to use
        """
    )
    
    # Documentation sources
    parser.add_argument(
        '--docs',
        required=False,
        nargs='+',
        metavar='PATH_OR_URL',
        help='Documentation sources (file paths, directory paths, or URLs). If not provided, loads from config file.'
    )
    
    parser.add_argument(
        '--config',
        metavar='FILE',
        help='Path to configuration file (default: searches for .doctai.yml/yaml/json)'
    )
    
    # API configuration
    # Note: API key default is set after config file is loaded
    parser.add_argument(
        '--api-key',
        default=None,
        metavar='KEY',
        help='API key for AI provider (or set DOCTAI_API_KEY env var, or configure api_key_env_var in config file)'
    )
    
    parser.add_argument(
        '--api-url',
        default=os.getenv('DOCTAI_API_URL'),
        metavar='URL',
        help='Custom API URL (or set DOCTAI_API_URL env var)'
    )
    
    parser.add_argument(
        '--provider',
        default=os.getenv('DOCTAI_PROVIDER', 'openai'),
        choices=['openai', 'anthropic', 'gemini', 'custom'],
        help='AI provider (default: openai, or set DOCTAI_PROVIDER env var)'
    )
    
    parser.add_argument(
        '--model',
        default=os.getenv('DOCTAI_MODEL'),
        metavar='MODEL',
        help='Model name to use (or set DOCTAI_MODEL env var)'
    )
    
    # Execution options
    parser.add_argument(
        '--work-dir',
        metavar='DIR',
        help='Working directory for test execution (creates temp dir if not specified)'
    )
    
    parser.add_argument(
        '--max-iterations',
        type=int,
        default=3,
        metavar='N',
        help='Maximum AI conversation iterations (default: 3)'
    )
    
    parser.add_argument(
        '--stop-on-failure',
        action='store_true',
        help='Stop executing scripts after first failure'
    )
    
    parser.add_argument(
        '--timeout',
        type=int,
        default=120,
        metavar='SECONDS',
        help='AI request timeout in seconds (default: 120)'
    )
    
    # Output options
    parser.add_argument(
        '--output',
        metavar='FILE',
        help='Save results to JSON file'
    )
    
    parser.add_argument(
        '--quiet',
        action='store_true',
        help='Suppress detailed output (only show summary)'
    )
    
    parser.add_argument(
        '--instructions',
        metavar='TEXT',
        help='Additional instructions for the AI (can also be specified in config file)'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version='%(prog)s 0.1.0'
    )
    
    args = parser.parse_args()
    
    # Load configuration file
    try:
        config_loader = ConfigLoader(config_path=args.config)
        config = config_loader.load()
        
        if config and not args.quiet:
            config_source = args.config or "default config file"
            print(f"Loaded configuration from: {config_source}")
        
        # Determine which environment variable to use for API key
        # Priority: DOCTAI_API_KEY_ENV_VAR > config file > default (DOCTAI_API_KEY)
        api_key_env_var = os.getenv('DOCTAI_API_KEY_ENV_VAR') or config_loader.get_api_key_env_var() or 'DOCTAI_API_KEY'
        
        # If no API key provided via CLI, read from the specified environment variable
        if args.api_key is None:
            args.api_key = os.getenv(api_key_env_var)
            if args.api_key and not args.quiet:
                print(f"Using API key from environment variable: {api_key_env_var}")
        
        # Merge config with command-line args (CLI takes precedence)
        merged_config = config_loader.merge_with_args(vars(args))
        
        # Update args with merged config
        for key, value in merged_config.items():
            setattr(args, key, value)
    
    except FileNotFoundError as e:
        parser.error(str(e))
    except Exception as e:
        print(f"Warning: Failed to load config file: {e}", file=sys.stderr)
        print("Continuing with command-line arguments only...", file=sys.stderr)
        # Still try to get API key from default env var if config loading failed
        if args.api_key is None:
            args.api_key = os.getenv('DOCTAI_API_KEY')
    
    # Validate we have documentation sources
    if not args.docs:
        parser.error("--docs is required or must be specified in config file")
    
    # Validate API key
    if not args.api_key:
        print("\n" + "="*80)
        print("ERROR: API Key Required")
        print("="*80)
        print("\nNo API key provided. Please provide an API key using one of these methods:\n")
        print("  1. Command line:")
        print("     doctai --api-key YOUR_API_KEY\n")
        print("  2. Environment variable:")
        print("     export DOCTAI_API_KEY='YOUR_API_KEY'")
        print("     doctai\n")
        print("  3. Custom environment variable (in config file):")
        print("     # .doctai.yml")
        print("     api_key_env_var: OPENAI_API_KEY  # or ANTHROPIC_API_KEY, etc.")
        print("     export OPENAI_API_KEY='YOUR_API_KEY'")
        print("     doctai\n")
        print("  4. Get an API key from:")
        print("     - OpenAI: https://platform.openai.com/api-keys")
        print("     - Anthropic (Claude): https://console.anthropic.com/")
        print("     - Gemini: https://aistudio.google.com/app/apikey")
        print("\n" + "="*80 + "\n")
        sys.exit(1)
    
    # Validate custom provider requirements
    if args.provider == 'custom':
        if not args.api_url:
            parser.error("--api-url is required when using custom provider")
        if not args.model:
            parser.error("--model is required when using custom provider")
    
    try:
        # Initialize AI client
        if not args.quiet:
            print(f"Initializing AI client (provider: {args.provider}, model: {args.model or 'default'})...")
        
        try:
            ai_client = AIClient(
                api_key=args.api_key,
                api_url=args.api_url,
                provider=args.provider,
                model=args.model,
                timeout=args.timeout
            )
        except ValueError as e:
            print("\n" + "="*80)
            print("ERROR: Invalid Configuration")
            print("="*80)
            print(f"\n{str(e)}")
            print(f"\nProvider: {args.provider}")
            print(f"Model: {args.model or 'default'}")
            print("\nValid providers: openai, anthropic, gemini, custom")
            print("\n" + "="*80 + "\n")
            sys.exit(1)
        except Exception as e:
            print("\n" + "="*80)
            print("ERROR: Failed to Initialize AI Client")
            print("="*80)
            print(f"\n{str(e)}")
            print(f"\nProvider: {args.provider}")
            print(f"Model: {args.model or 'default'}")
            print("\nPlease check:")
            print("  - API key is valid")
            print("  - Provider name is correct (openai, anthropic, gemini)")
            print("  - Model name is correct")
            print("\n" + "="*80 + "\n")
            sys.exit(1)
        
        # Initialize documentation tester
        tester = DocumentationTester(
            ai_client=ai_client,
            work_dir=args.work_dir,
            verbose=not args.quiet
        )
        
        # Run tests
        results = tester.test_documentation(
            sources=args.docs,
            max_iterations=args.max_iterations,
            stop_on_failure=args.stop_on_failure,
            custom_instructions=args.instructions
        )
        
        # Save results to file if requested
        if args.output:
            with open(args.output, 'w') as f:
                json.dump(results, f, indent=2)
            print(f"\nResults saved to: {args.output}")
        
        # Exit with appropriate code
        sys.exit(0 if results['success'] else 1)
    
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
        sys.exit(130)
    
    except Exception as e:
        print("\n" + "="*80)
        print("ERROR: Unexpected Error")
        print("="*80)
        print(f"\n{type(e).__name__}: {str(e)}")
        
        # Print more details for common errors
        error_str = str(e).lower()
        if "api" in error_str or "authentication" in error_str or "401" in error_str:
            print("\nThis appears to be an API authentication error. Please check:")
            print("  - API key is valid and has not expired")
            print("  - API key is for the correct provider (OpenAI, Anthropic, Gemini)")
            print("  - You have credits/quota remaining")
        
        if "rate limit" in error_str or "429" in error_str:
            print("\nRate limit exceeded. Try:")
            print("  - Wait a few moments and try again")
            print("  - Use a different API key")
            print("  - Check your provider's rate limits")
        
        if "timeout" in error_str or "timed out" in error_str:
            print("\nRequest timed out. Try:")
            print("  - Increase timeout with --timeout 300")
            print("  - Check your internet connection")
            print("  - Try again later")
        
        if not args.quiet:
            import traceback
            print("\nFull traceback:")
            print("-" * 80)
            traceback.print_exc()
        
        print("\n" + "="*80 + "\n")
        sys.exit(1)


if __name__ == '__main__':
    main()

