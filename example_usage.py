#!/usr/bin/env python3
"""
Example usage of the Git Zip Extractor Tool
"""

from git_zip_to_pdf import GitZipExtractor


def example_basic_usage():
    """Basic usage example."""
    print("Example 1: Basic usage")
    print("-" * 50)

    # Process a zip file with default output directory
    try:
        extractor = GitZipExtractor("my-repository.zip")
        extractor.process()
    except FileNotFoundError:
        print("Example zip file not found. Please provide a valid zip file.")
    except Exception as e:
        print(f"Error: {e}")


def example_custom_output():
    """Example with custom output directory."""
    print("\nExample 2: Custom output directory")
    print("-" * 50)

    try:
        extractor = GitZipExtractor(
            zip_path="my-repository.zip",
            output_dir="custom_output"
        )
        extractor.process()
    except FileNotFoundError:
        print("Example zip file not found. Please provide a valid zip file.")
    except Exception as e:
        print(f"Error: {e}")


def example_programmatic():
    """Example of using the tool programmatically with more control."""
    print("\nExample 3: Programmatic usage")
    print("-" * 50)

    try:
        # Initialize extractor
        extractor = GitZipExtractor("my-repository.zip", "my_output")

        # Extract zip
        extractor.extract_zip()

        # Collect files
        files_data = extractor.collect_files()
        print(f"Found {len(files_data)} files")

        # You can inspect or modify files_data here
        for file_info in files_data[:5]:  # Show first 5 files
            print(f"  - {file_info['path']}")

        # Generate outputs
        text_file = extractor.generate_text_file(files_data)
        pdf_file = extractor.generate_pdf(files_data)

        print(f"\nGenerated:")
        print(f"  Text: {text_file}")
        print(f"  PDF: {pdf_file}")

    except FileNotFoundError:
        print("Example zip file not found. Please provide a valid zip file.")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    print("Git Zip Extractor - Usage Examples")
    print("=" * 50)
    print()

    # Uncomment the example you want to run:

    # example_basic_usage()
    # example_custom_output()
    # example_programmatic()

    print("\nTo use these examples:")
    print("1. Uncomment the example function you want to run")
    print("2. Replace 'my-repository.zip' with your actual zip file")
    print("3. Run: python example_usage.py")
    print()
    print("Or use the command line tool directly:")
    print("  python git_zip_to_pdf.py your-file.zip")
