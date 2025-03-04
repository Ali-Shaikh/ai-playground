import ollama
import os
import re
from pathlib import Path
from datetime import datetime


def generate_landing_page(description):
    """Use Ollama to generate HTML/CSS for a landing page based on description."""
    messages = [
        {"role": "system",
         "content": "You are a skilled web developer who creates clean, responsive landing pages using HTML, CSS, and minimal JavaScript. Your code should be complete, valid, and ready to use without external dependencies."},
        {"role": "user",
         "content": f"Create a complete landing page based on this description: {description}. Provide only the HTML code with internal CSS and JavaScript. The code should be complete and ready to be saved as an index.html file."}
    ]

    try:
        print("Generating landing page... This may take a minute or two...")
        response = ollama.chat(
            model='deepseek-r1:8b',
            messages=messages
        )

        # Extract HTML code from response
        html_content = response['message']['content']

        # Extract code between ```html and ``` if present
        code_pattern = re.compile(r'```(?:html)?\s*([\s\S]*?)\s*```')
        match = code_pattern.search(html_content)

        if match:
            return match.group(1).strip()
        else:
            # If no code blocks found, try to extract just the HTML
            if "<html" in html_content and "</html>" in html_content:
                start = html_content.find("<html")
                end = html_content.find("</html>") + 7
                return html_content[start:end]
            return html_content

    except Exception as e:
        return f"Error generating landing page: {str(e)}"


def save_landing_page(html_content, output_dir="landing_pages"):
    """Save the generated HTML to a file."""
    # Ensure the output directory exists
    Path(output_dir).mkdir(exist_ok=True)

    # Create a filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{output_dir}/landing_page_{timestamp}.html"

    # Save the HTML content
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html_content)

    return filename


def main():
    """Run the dedicated landing page generator."""
    print("==========================================")
    print("  LANDING PAGE GENERATOR (OLLAMA)  ")
    print("==========================================")

    # Get description for the landing page
    print("\nDescribe the landing page you want (be specific about colors, layout, features):")
    description = input("> ")

    if not description:
        print("Error: You must provide a description for the landing page.")
        return

    # Generate the landing page HTML
    html_content = generate_landing_page(description)

    # Save the landing page
    filename = save_landing_page(html_content)

    print(f"\nSuccess! Landing page created and saved to: {filename}")

    # Ask if user wants to open the file
    open_file = input("Would you like to open the landing page now? (y/n): ")
    if open_file.lower() in ['y', 'yes']:
        # Try to open the file in the default browser
        try:
            import webbrowser
            file_path = os.path.abspath(filename)
            webbrowser.open('file://' + file_path)
            print(f"Opened {filename} in your default browser.")
        except Exception as e:
            print(f"Couldn't open the file automatically: {e}")
            print(f"Please open {filename} manually in your browser.")

    # Ask if user wants to create another landing page
    another = input("\nWould you like to create another landing page? (y/n): ")
    if another.lower() in ['y', 'yes']:
        main()  # Recursive call
    else:
        print("Thank you for using the Landing Page Generator. Goodbye!")


if __name__ == "__main__":
    main()