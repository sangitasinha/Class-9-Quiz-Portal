import json
import os
from pathlib import Path


def convert_text_to_json():
    """
    Convert text files to JSON format for the quiz portal
    This script reads text files in a specific format and converts them to JSON
    """

    # Create directories
    os.makedirs("quiz_data", exist_ok=True)
    os.makedirs("try1/text_data", exist_ok=True)

    def parse_quiz_text(text_content, filename):
        """
        Parse the text content from text files into structured data
        """
        try:
            # Clean the text content
            text_content = text_content.strip()

            # Remove any leading/trailing quotes or commas if present
            if text_content.startswith('"') and text_content.endswith(','):
                text_content = text_content[1:-1]
            elif text_content.startswith('"') and text_content.endswith('"'):
                text_content = text_content[1:-1]

            # If the content doesn't start with {, wrap it
            if not text_content.startswith('{'):
                text_content = '{' + text_content + '}'

            # Parse the JSON structure
            data = json.loads(text_content)
            return data

        except json.JSONDecodeError as e:
            print(f"❌ Error parsing {filename}: {e}")
            print(f"💡 Check the JSON syntax in {filename}")
            return None
        except Exception as e:
            print(f"❌ Unexpected error with {filename}: {e}")
            return None

    def convert_existing_text_files():
        """
        Convert any existing text files in text_data folder to JSON
        """
        text_data_path = Path("try1/text_data")
        converted_files = []

        if not text_data_path.exists():
            print("📁 text_data folder not found, creating it...")
            return converted_files

        # Look for text files
        for txt_file in text_data_path.glob("*.txt"):
            if txt_file.name == "template.txt":
                continue  # Skip template file

            print(f"🔄 Processing {txt_file.name}...")

            try:
                with open(txt_file, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Parse the content
                parsed_data = parse_quiz_text(content, txt_file.name)

                if parsed_data:
                    # Generate output filename
                    output_name = txt_file.stem + ".json"
                    output_path = Path("quiz_data") / output_name

                    # Save to JSON
                    with open(output_path, 'w', encoding='utf-8') as f:
                        json.dump(parsed_data, f, indent=4, ensure_ascii=False)

                    converted_files.append(output_name)
                    print(f"✅ {txt_file.name} → {output_name}")
                else:
                    print(f"❌ Failed to convert {txt_file.name}")

            except FileNotFoundError:
                print(f"❌ File not found: {txt_file}")
            except Exception as e:
                print(f"❌ Error processing {txt_file}: {e}")

        return converted_files

    # First, convert any existing text files
    print("🔍 Looking for existing text files to convert...")
    converted_files = convert_existing_text_files()

    if converted_files:
        print(f"\n✅ Converted {len(converted_files)} file(s):")
        for file in converted_files:
            print(f"   - {file}")
    else:
        print("📝 No text files found to convert. Creating sample data...")

    # Create sample data if no files were converted or if sample files don't exist
    sample_files_needed = []
    required_files = ["civics.json", "history.json", "geography.json", "economics.json"]

    for file in required_files:
        if not Path(f"quiz_data/{file}").exists():
            sample_files_needed.append(file)

    if sample_files_needed:
        print(f"\n🔧 Creating sample data for: {', '.join(sample_files_needed)}")

        # Create the sample data you provided
        if "civics.json" in sample_files_needed:
            create_civics_data()
        if "history.json" in sample_files_needed:
            create_sample_history_data()
        if "geography.json" in sample_files_needed:
            create_sample_geography_data()
        if "economics.json" in sample_files_needed:
            create_sample_economics_data()

    print("\n🎉 Data conversion complete!")
    print("\n📁 Available quiz data files:")
    quiz_data_path = Path("quiz_data")
    if quiz_data_path.exists():
        for json_file in quiz_data_path.glob("*.json"):
            # Load and count questions
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                question_count = count_questions(data)
                print(f"   ✅ {json_file.name} - {question_count} questions")
            except:
                print(f"   📄 {json_file.name}")


def count_questions(data):
    """Count total questions in a data structure"""
    total = 0
    for subject, chapters in data.items():
        for chapter, sections in chapters.items():
            for section, questions in sections.items():
                if isinstance(questions, list):
                    total += len(questions)
    return total


def create_civics_data():
    """Create the civics data from your original paste"""
    civics_data = {
        "Civics": {
            "Chapter 1: Democracy in the Contemporary World": {
                "What is Democracy?": [
                    {
                        "question": "What does the word 'democracy' mean?",
                        "options": ["Rule by the rich", "Rule by the people", "Rule by the military",
                                    "Rule by the educated"],
                        "correct_answer": 1,
                        "explanation": "Democracy comes from the Greek words 'demos' (people) and 'kratia' (rule), meaning rule by the people."
                    },
                    {
                        "question": "In which country did democracy originate?",
                        "options": ["Rome", "Greece", "Egypt", "India"],
                        "correct_answer": 1,
                        "explanation": "Democracy originated in ancient Greece, particularly in Athens around the 5th century BCE."
                    },
                    {
                        "question": "What is the key feature of democracy?",
                        "options": ["Rule by one person", "Rule by few people",
                                    "Rule by majority with respect for minority", "Rule by the wealthy"],
                        "correct_answer": 2,
                        "explanation": "The key feature of democracy is rule by majority while respecting the rights and opinions of minorities."
                    },
                    {
                        "question": "In a democracy, the final decision-making power rests with:",
                        "options": ["The army", "The wealthy class", "The people", "Religious leaders"],
                        "correct_answer": 2,
                        "explanation": "In a democracy, the final decision-making power rests with the people, either directly or through their elected representatives."
                    },
                    {
                        "question": "Which of these is NOT a feature of democracy?",
                        "options": ["Free and fair elections", "Rule of law", "Hereditary rule",
                                    "Protection of rights"],
                        "correct_answer": 2,
                        "explanation": "Hereditary rule is not a feature of democracy. In democracy, leaders are elected by the people, not born into power."
                    }
                ],
                "Features of Democracy": [
                    {
                        "question": "Elections in a democracy should be:",
                        "options": ["Held once in 10 years", "Free and fair", "Only for educated people",
                                    "Controlled by the government"],
                        "correct_answer": 1,
                        "explanation": "Elections in a democracy must be free and fair, allowing people to choose their representatives without coercion or fraud."
                    },
                    {
                        "question": "Universal Adult Franchise means:",
                        "options": ["Only adults can vote", "All adults have the right to vote",
                                    "Only educated adults can vote", "Only wealthy adults can vote"],
                        "correct_answer": 1,
                        "explanation": "Universal Adult Franchise means all adult citizens have the right to vote, regardless of their gender, religion, race, or economic status."
                    },
                    {
                        "question": "In India, the minimum voting age is:",
                        "options": ["16 years", "18 years", "21 years", "25 years"],
                        "correct_answer": 1,
                        "explanation": "In India, the minimum voting age is 18 years, lowered from 21 years in 1989."
                    },
                    {
                        "question": "What is meant by 'one person, one vote, one value'?",
                        "options": ["Everyone gets multiple votes", "Each vote has equal weight",
                                    "Only one person can vote", "Votes have different values"],
                        "correct_answer": 1,
                        "explanation": "This principle means that each person has one vote and each vote has equal weight regardless of the voter's social or economic status."
                    },
                    {
                        "question": "Rule of law in democracy means:",
                        "options": ["Only laws rule, not people", "Laws apply equally to all",
                                    "Rich people are above law", "Leaders can change laws anytime"],
                        "correct_answer": 1,
                        "explanation": "Rule of law means that laws apply equally to all citizens, including leaders and government officials."
                    }
                ]
            }
        }
    }

    with open("quiz_data/civics.json", "w", encoding="utf-8") as f:
        json.dump(civics_data, f, indent=4, ensure_ascii=False)
    print("✅ Created civics.json with original data")


def create_sample_history_data():
    """Create sample history data"""
    history_data = {
        "History": {
            "Chapter 1: The French Revolution": {
                "Causes of French Revolution": [
                    {
                        "question": "Which class paid most of the taxes in France before the revolution?",
                        "options": ["First Estate", "Second Estate", "Third Estate", "Nobility"],
                        "correct_answer": 2,
                        "explanation": "The Third Estate, comprising 98% of the population, bore the burden of taxation while the privileged First and Second Estates were exempt."
                    },
                    {
                        "question": "What was the immediate cause of the French Revolution?",
                        "options": ["Food shortage", "Financial crisis", "Social inequality", "Political corruption"],
                        "correct_answer": 1,
                        "explanation": "The immediate cause was the acute financial crisis faced by the French government due to wars and lavish spending."
                    }
                ],
                "Major Events": [
                    {
                        "question": "When did the French Revolution begin?",
                        "options": ["1787", "1789", "1791", "1793"],
                        "correct_answer": 1,
                        "explanation": "The French Revolution began in 1789 with the convening of the Estates-General and the Tennis Court Oath."
                    }
                ]
            }
        }
    }

    with open("quiz_data/history.json", "w", encoding="utf-8") as f:
        json.dump(history_data, f, indent=4, ensure_ascii=False)


def create_sample_geography_data():
    """Create sample geography data"""
    geography_data = {
        "Geography": {
            "Chapter 1: India - Size and Location": {
                "Location and Extent": [
                    {
                        "question": "Which meridian is taken as the Standard Meridian of India?",
                        "options": ["80°30'E", "82°30'E", "85°30'E", "90°30'E"],
                        "correct_answer": 1,
                        "explanation": "82°30'E longitude is taken as the Standard Meridian of India, passing through Mirzapur in Uttar Pradesh."
                    },
                    {
                        "question": "India's total area is approximately:",
                        "options": ["2.8 million sq km", "3.28 million sq km", "4.2 million sq km",
                                    "5.1 million sq km"],
                        "correct_answer": 1,
                        "explanation": "India has a total area of approximately 3.28 million square kilometers, making it the 7th largest country in the world."
                    }
                ]
            }
        }
    }

    with open("quiz_data/geography.json", "w", encoding="utf-8") as f:
        json.dump(geography_data, f, indent=4, ensure_ascii=False)


def create_sample_economics_data():
    """Create sample economics data"""
    economics_data = {
        "Economics": {
            "Chapter 1: The Story of Village Palampur": {
                "Farming in Palampur": [
                    {
                        "question": "What is the main economic activity in Palampur?",
                        "options": ["Manufacturing", "Farming", "Trade", "Services"],
                        "correct_answer": 1,
                        "explanation": "Farming is the main economic activity in Palampur, with 75% of people depending on it for their livelihood."
                    },
                    {
                        "question": "Which crop is grown in Palampur during the rainy season?",
                        "options": ["Wheat", "Sugarcane", "Jowar and Bajra", "Potato"],
                        "correct_answer": 2,
                        "explanation": "Jowar and Bajra are grown during the rainy (kharif) season in Palampur."
                    }
                ]
            }
        }
    }

    with open("quiz_data/economics.json", "w", encoding="utf-8") as f:
        json.dump(economics_data, f, indent=4, ensure_ascii=False)


def create_text_template():
    """Create a template file showing the expected text format"""
    template = '''# Text Data Format Template for Quiz Portal
# Save your quiz data in this format and run the converter script

{
    "Subject Name": {
        "Chapter Name": {
            "Section Name": [
                {
                    "question": "Your question here?",
                    "options": ["Option A", "Option B", "Option C", "Option D"],
                    "correct_answer": 0,
                    "explanation": "Explanation for the correct answer."
                },
                {
                    "question": "Another question?",
                    "options": ["Option A", "Option B", "Option C", "Option D"],
                    "correct_answer": 1,
                    "explanation": "Another explanation."
                }
            ],
            "Another Section": [
                {
                    "question": "Question for another section?",
                    "options": ["Option A", "Option B", "Option C", "Option D"],
                    "correct_answer": 2,
                    "explanation": "Explanation for this question."
                }
            ]
        },
        "Another Chapter": {
            "Section in Second Chapter": [
                {
                    "question": "Question in second chapter?",
                    "options": ["Option A", "Option B", "Option C", "Option D"],
                    "correct_answer": 3,
                    "explanation": "Explanation for second chapter question."
                }
            ]
        }
    }
}

# IMPORTANT NOTES:
# 1. correct_answer is the INDEX (0, 1, 2, or 3) of the correct option
# 2. Make sure to use proper JSON formatting with quotes and commas
# 3. Always provide exactly 4 options
# 4. Include detailed explanations for learning
# 5. Each subject should be in a separate .txt file
# 6. Recommended file names: civics.txt, history.txt, geography.txt, economics.txt

# EXAMPLE FILE STRUCTURE:
# text_data/
# ├── civics.txt      (Contains Civics subject data)
# ├── history.txt     (Contains History subject data)  
# ├── geography.txt   (Contains Geography subject data)
# └── economics.txt   (Contains Economics subject data)

# After creating your text files, run: python data_converter.py
'''

    os.makedirs("try1/text_data", exist_ok=True)
    with open("try1/text_data/template.txt", "w", encoding="utf-8") as f:
        f.write(template)

    print("📄 Template file created at: text_data/template.txt")


def create_sample_text_files():
    """Create sample text files that users can modify"""

    # Sample Civics text file
    civics_sample = '''{
    "Civics": {
        "Chapter 1: Democracy in the Contemporary World": {
            "What is Democracy?": [
                {
                    "question": "What does the word 'democracy' mean?",
                    "options": ["Rule by the rich", "Rule by the people", "Rule by the military", "Rule by the educated"],
                    "correct_answer": 1,
                    "explanation": "Democracy comes from the Greek words 'demos' (people) and 'kratia' (rule), meaning rule by the people."
                }
            ]
        }
    }
}'''

    # Sample History text file
    history_sample = '''{
    "History": {
        "Chapter 1: The French Revolution": {
            "Causes of Revolution": [
                {
                    "question": "Which estate paid most of the taxes in France?",
                    "options": ["First Estate", "Second Estate", "Third Estate", "All equally"],
                    "correct_answer": 2,
                    "explanation": "The Third Estate bore most of the tax burden while the privileged estates were largely exempt."
                }
            ]
        }
    }
}'''

    # Create sample files
    samples = {
        "civics_sample.txt": civics_sample,
        "history_sample.txt": history_sample
    }

    for filename, content in samples.items():
        filepath = f"text_data/{filename}"
        if not Path(filepath).exists():
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"📝 Created sample file: {filename}")


def validate_quiz_data(data, filename):
    """Validate the structure of quiz data"""
    errors = []
    warnings = []

    try:
        for subject_name, chapters in data.items():
            if not isinstance(chapters, dict):
                errors.append(f"Subject '{subject_name}' should contain chapters (dict)")
                continue

            for chapter_name, sections in chapters.items():
                if not isinstance(sections, dict):
                    errors.append(f"Chapter '{chapter_name}' should contain sections (dict)")
                    continue

                for section_name, questions in sections.items():
                    if not isinstance(questions, list):
                        errors.append(f"Section '{section_name}' should contain questions (list)")
                        continue

                    for i, question in enumerate(questions):
                        if not isinstance(question, dict):
                            errors.append(f"Question {i + 1} in '{section_name}' should be a dict")
                            continue

                        # Check required fields
                        required_fields = ["question", "options", "correct_answer", "explanation"]
                        for field in required_fields:
                            if field not in question:
                                errors.append(f"Question {i + 1} in '{section_name}' missing '{field}'")

                        # Validate options
                        if "options" in question:
                            if not isinstance(question["options"], list):
                                errors.append(f"Options in question {i + 1} should be a list")
                            elif len(question["options"]) != 4:
                                warnings.append(f"Question {i + 1} in '{section_name}' should have exactly 4 options")

                        # Validate correct_answer
                        if "correct_answer" in question:
                            if not isinstance(question["correct_answer"], int):
                                errors.append(f"correct_answer in question {i + 1} should be an integer")
                            elif question["correct_answer"] not in [0, 1, 2, 3]:
                                errors.append(f"correct_answer in question {i + 1} should be 0, 1, 2, or 3")

    except Exception as e:
        errors.append(f"Unexpected error during validation: {e}")

    # Report validation results
    if errors:
        print(f"❌ Validation errors in {filename}:")
        for error in errors:
            print(f"   - {error}")

    if warnings:
        print(f"⚠️ Validation warnings in {filename}:")
        for warning in warnings:
            print(f"   - {warning}")

    if not errors and not warnings:
        print(f"✅ {filename} passed validation")

    return len(errors) == 0  # Return True if no errors


def interactive_mode():
    """Interactive mode for creating quiz data"""
    print("\n🎯 Interactive Quiz Creator")
    print("=" * 40)

    subject = input("Enter subject name (e.g., History): ").strip()
    chapter = input("Enter chapter name: ").strip()
    section = input("Enter section name: ").strip()

    questions = []

    while True:
        print(f"\n📝 Adding question {len(questions) + 1}:")

        question_text = input("Enter question: ").strip()
        if not question_text:
            break

        options = []
        for i in range(4):
            option = input(f"Option {chr(65 + i)}: ").strip()
            options.append(option)

        while True:
            try:
                correct = int(input("Correct answer (0, 1, 2, or 3): "))
                if correct in [0, 1, 2, 3]:
                    break
                else:
                    print("Please enter 0, 1, 2, or 3")
            except ValueError:
                print("Please enter a number")

        explanation = input("Explanation: ").strip()

        question_obj = {
            "question": question_text,
            "options": options,
            "correct_answer": correct,
            "explanation": explanation
        }

        questions.append(question_obj)

        if input("\nAdd another question? (y/n): ").lower() != 'y':
            break

    if questions:
        data = {
            subject: {
                chapter: {
                    section: questions
                }
            }
        }

        filename = f"text_data/{subject.lower()}_interactive.txt"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

        print(f"\n✅ Created {filename} with {len(questions)} questions!")

        # Convert to JSON immediately
        converted_data = convert_single_file(filename)
        if converted_data:
            print("🔄 Automatically converted to JSON format!")


def convert_single_file(filepath):
    """Convert a single text file to JSON"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        data = json.loads(content)

        # Validate the data
        if validate_quiz_data(data, Path(filepath).name):
            # Save to JSON
            json_filename = Path(filepath).stem + ".json"
            json_path = Path("quiz_data") / json_filename

            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)

            return data
        else:
            return None

    except Exception as e:
        print(f"❌ Error converting {filepath}: {e}")
        return None


if __name__ == "__main__":
    print("🔄 Class 9 Social Science Quiz Data Converter")
    print("=" * 50)

    # Check command line arguments for different modes
    import sys

    if len(sys.argv) > 1:
        if sys.argv[1] == "interactive" or sys.argv[1] == "-i":
            interactive_mode()
            sys.exit()
        elif sys.argv[1] == "help" or sys.argv[1] == "-h":
            print("""
📚 Quiz Data Converter - Usage Guide

Basic Usage:
  python data_converter.py              # Convert all text files + create samples
  python data_converter.py interactive  # Interactive question creator
  python data_converter.py help         # Show this help

File Structure:
  text_data/       # Your input text files (.txt)
  quiz_data/       # Generated JSON files (.json)

Supported Commands:
  -i, interactive  # Interactive mode to create questions
  -h, help        # Show this help message

Text File Format:
  - Use JSON format in .txt files
  - Each subject in separate file
  - Structure: Subject > Chapter > Section > Questions

Example Files:
  text_data/civics.txt
  text_data/history.txt
  text_data/geography.txt
  text_data/economics.txt
            """)
            sys.exit()

    # Main conversion process
    print("🔍 Starting conversion process...")
    convert_text_to_json()
    create_text_template()
    create_sample_text_files()

    print("\n" + "=" * 50)
    print("✅ Setup Complete!")
    print("\n📋 Next Steps:")
    print("1. Edit files in text_data/ folder with your quiz questions")
    print("2. Run 'python data_converter.py' again to convert updates")
    print("3. Run 'streamlit run main_app.py' to start the quiz portal")
    print("\n💡 Tips:")
    print("- Use 'python data_converter.py interactive' for guided question creation")
    print("- Check text_data/template.txt for format reference")
    print("- Validate your JSON format before converting")