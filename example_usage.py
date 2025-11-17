#!/usr/bin/env python3
"""
Example usage of the Advanced Git Zip Extractor Tool
"""

from git_zip_to_pdf import AdvancedGitZipExtractor
import json


def example_basic_usage():
    """Basic usage example."""
    print("=" * 80)
    print("Example 1: Basic Usage")
    print("=" * 80)
    print()

    # Process a zip file with default settings
    # This will create all output formats (PDF, HTML, Markdown, Text, JSON)
    try:
        extractor = AdvancedGitZipExtractor("my-repository.zip")
        extractor.process()
    except FileNotFoundError:
        print("❌ Example zip file not found. Please provide a valid zip file.")
        print("   Download a repository as ZIP from GitHub to test.")
    except Exception as e:
        print(f"❌ Error: {e}")


def example_custom_output():
    """Example with custom output directory."""
    print("\n" + "=" * 80)
    print("Example 2: Custom Output Directory")
    print("=" * 80)
    print()

    try:
        # Specify custom output directory
        extractor = AdvancedGitZipExtractor(
            zip_path="my-repository.zip",
            output_dir="custom_output"
        )
        extractor.process()
    except FileNotFoundError:
        print("❌ Example zip file not found.")
    except Exception as e:
        print(f"❌ Error: {e}")


def example_with_config():
    """Example using configuration file."""
    print("\n" + "=" * 80)
    print("Example 3: Using Configuration File")
    print("=" * 80)
    print()

    try:
        # Use custom configuration
        extractor = AdvancedGitZipExtractor(
            zip_path="my-repository.zip",
            output_dir="configured_output",
            config_file="config.example.json"
        )
        extractor.process()
    except FileNotFoundError:
        print("❌ Example zip file not found.")
    except Exception as e:
        print(f"❌ Error: {e}")


def example_custom_config():
    """Example with inline configuration."""
    print("\n" + "=" * 80)
    print("Example 4: Custom Configuration (Inline)")
    print("=" * 80)
    print()

    try:
        # Create custom config
        custom_config = {
            'max_lines_in_pdf': 2000,
            'font_size': 9,
            'page_size': 'A4',
            'generate_html': True,
            'generate_markdown': False,  # Skip markdown
            'syntax_highlighting': True,
        }

        # Save custom config
        config_path = "temp_config.json"
        with open(config_path, 'w') as f:
            json.dump(custom_config, f, indent=2)

        # Use custom config
        extractor = AdvancedGitZipExtractor(
            zip_path="my-repository.zip",
            output_dir="custom_config_output",
            config_file=config_path
        )
        extractor.process()

    except FileNotFoundError:
        print("❌ Example zip file not found.")
    except Exception as e:
        print(f"❌ Error: {e}")


def example_programmatic():
    """Example of using the tool programmatically with more control."""
    print("\n" + "=" * 80)
    print("Example 5: Programmatic Usage with Fine Control")
    print("=" * 80)
    print()

    try:
        # Initialize extractor
        extractor = AdvancedGitZipExtractor("my-repository.zip", "programmatic_output")

        # Override specific config options
        extractor.config['generate_html'] = True
        extractor.config['generate_markdown'] = True
        extractor.config['max_lines_in_pdf'] = 1500

        # Extract zip
        print("📦 Extracting repository...")
        extractor.extract_zip()

        # Collect files
        print("📂 Collecting and analyzing files...")
        files_data = extractor.collect_files()
        print(f"✓ Found {len(files_data)} files to process")

        # Display file list
        print("\n📄 Files to process:")
        for i, file_info in enumerate(files_data[:10], 1):  # Show first 10
            print(f"   {i:2d}. {file_info['path']} ({file_info['language']})")
        if len(files_data) > 10:
            print(f"   ... and {len(files_data) - 10} more files")

        # Generate specific outputs
        print("\n📝 Generating outputs...")

        # Text output
        text_file = extractor.generate_text_file(files_data)
        print(f"   ✓ Text: {text_file}")

        # HTML output
        html_file = extractor.generate_html(files_data)
        print(f"   ✓ HTML: {html_file}")

        # Markdown output
        md_file = extractor.generate_markdown(files_data)
        print(f"   ✓ Markdown: {md_file}")

        # PDF output
        pdf_file = extractor.generate_pdf(files_data)
        if pdf_file:
            print(f"   ✓ PDF: {pdf_file}")

        # Statistics JSON
        extractor.save_stats_json()

        # Display statistics
        print("\n📊 Repository Statistics:")
        print(extractor.generate_stats_report())

    except FileNotFoundError:
        print("❌ Example zip file not found. Please provide a valid zip file.")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()


def example_stats_only():
    """Example: Just get statistics without generating full outputs."""
    print("\n" + "=" * 80)
    print("Example 6: Statistics Only")
    print("=" * 80)
    print()

    try:
        # Initialize extractor
        extractor = AdvancedGitZipExtractor("my-repository.zip", "stats_output")

        # Disable all outputs
        extractor.config['generate_html'] = False
        extractor.config['generate_markdown'] = False

        # Extract and collect
        extractor.extract_zip()
        files_data = extractor.collect_files()

        # Just save statistics
        extractor.save_stats_json()

        # Print statistics
        print(extractor.generate_stats_report())

        # Access stats programmatically
        stats = extractor.repo_stats.get_summary()
        print(f"\n📈 Quick Stats:")
        print(f"   Total Files: {stats['total_files']:,}")
        print(f"   Total Lines: {stats['total_lines']:,}")
        print(f"   Total Size: {extractor.format_size(stats['total_size'])}")

        print("\n   Top 5 Languages:")
        sorted_langs = sorted(
            stats['languages'].items(),
            key=lambda x: x[1]['lines'],
            reverse=True
        )[:5]

        for lang, lang_stats in sorted_langs:
            percentage = (lang_stats['lines'] / stats['total_lines'] * 100)
            print(f"   • {lang.capitalize()}: {lang_stats['lines']:,} lines ({percentage:.1f}%)")

    except FileNotFoundError:
        print("❌ Example zip file not found.")
    except Exception as e:
        print(f"❌ Error: {e}")


def example_selective_outputs():
    """Example: Generate only specific output formats."""
    print("\n" + "=" * 80)
    print("Example 7: Selective Output Formats")
    print("=" * 80)
    print()

    try:
        # PDF and HTML only, skip Markdown and Text
        extractor = AdvancedGitZipExtractor("my-repository.zip", "selective_output")

        extractor.config['generate_markdown'] = False

        # Extract and process
        extractor.extract_zip()
        files_data = extractor.collect_files()

        # Generate only PDF and HTML
        extractor.generate_pdf(files_data)
        extractor.generate_html(files_data)

        print("✓ Generated PDF and HTML only")

    except FileNotFoundError:
        print("❌ Example zip file not found.")
    except Exception as e:
        print(f"❌ Error: {e}")


def show_usage_instructions():
    """Display usage instructions."""
    print("\n" + "=" * 80)
    print("ADVANCED GIT ZIP EXTRACTOR - USAGE EXAMPLES")
    print("=" * 80)
    print()
    print("To run these examples:")
    print()
    print("1. First, download a repository as ZIP from GitHub:")
    print("   • Go to any GitHub repository")
    print("   • Click 'Code' → 'Download ZIP'")
    print("   • Save it as 'my-repository.zip' in this directory")
    print()
    print("2. Uncomment the example you want to run below")
    print()
    print("3. Run this script:")
    print("   python example_usage.py")
    print()
    print("Available examples:")
    print("  • example_basic_usage()         - Basic usage with all defaults")
    print("  • example_custom_output()       - Custom output directory")
    print("  • example_with_config()         - Using config file")
    print("  • example_custom_config()       - Inline custom configuration")
    print("  • example_programmatic()        - Full programmatic control")
    print("  • example_stats_only()          - Just get statistics")
    print("  • example_selective_outputs()   - Generate specific formats only")
    print()
    print("=" * 80)


if __name__ == "__main__":
    show_usage_instructions()

    # Uncomment the example you want to run:

    # example_basic_usage()
    # example_custom_output()
    # example_with_config()
    # example_custom_config()
    # example_programmatic()
    # example_stats_only()
    # example_selective_outputs()

    print("\n💡 Tip: Uncomment one of the example functions above to run it!")
