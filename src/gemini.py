from dotenv import load_dotenv
from google import genai

load_dotenv()

def main():
    client = genai.Client()
    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents="This is a test message. Please simply let me know if you are working."
    )
    print(response.text)

if __name__ == "__main__":
    main()
