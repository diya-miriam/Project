from fastapi import FastAPI
from fastapi.responses import JSONResponse
from firecrawl import FirecrawlApp
import google.generativeai as genai

# Configure the generative AI model with your API key
genai.configure(api_key="apikey")

# Initialize Firecrawl app with API key
app = FirecrawlApp(api_key="apikey")

# FastAPI app initialization
fastapi_app = FastAPI()

# Define the username (example: hydantess)
username = 'hydantess'  # Example based on the response

# Crawl the website with Firecrawl
def get_kaggle_data(username: str):
    crawl_status = app.crawl_url(
        f'https://kaggle.com/{username}',  # URL with the username
        params={
            'limit': 100,
            'scrapeOptions': {'formats': ['markdown']}
        }
    )

    # Check if the crawl was successful
    if crawl_status['status'] == 'completed':
        # Prepare a simple prompt using the full crawl_status
        prompt = f"Extract relevant information from the following crawl data:\n{str(crawl_status)}"

        # Create and call the Gemini model
        try:
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(prompt)

            # Return the response text
            return response.text
        except Exception as e:
            return f"Error generating content: {e}"
    else:
        return f"Error in Firecrawl API: {crawl_status}"

# Define a route to display Kaggle data for the username
@fastapi_app.get("/", response_class=JSONResponse)
async def read_root():
    # Fetch the Kaggle data for the user
    generated_content = get_kaggle_data(username)

    # Return the content as a JSON response
    return JSONResponse(content={"generated_content": generated_content})

# To run the app, use Uvicorn from the terminal:
# uvicorn your_filename:fastapi_app --reload
