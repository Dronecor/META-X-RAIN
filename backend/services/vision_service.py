import os
from groq import Groq
from backend.config import settings

class VisionService:
    def __init__(self):
        self.client = Groq(api_key=settings.GROQ_API_KEY)
        self.model = "llama-3.2-11b-vision-preview" # Using Llama 3.2 Vision

    def analyze_image(self, image_url: str) -> str:
        """
        Analyzes an image and returns a detailed visual description suitable for search matching.
        """
        if not image_url:
            return ""

        print(f"Analyzing image: {image_url}")
        try:
            # Handle local files (starting with /static or similar)
            is_local = image_url.startswith("/static") or "localhost" in image_url
            
            messages_content = []
            
            if is_local:
                # Convert to base64
                import base64
                
                # Assume relative path for /static
                if image_url.startswith("/static"):
                    file_path = f"backend{image_url}"
                elif "localhost" in image_url:
                    # Strip domain to get path
                    # This is brittle, assuming standard structure
                    path_part = image_url.split("8000")[-1]
                    file_path = f"backend{path_part}"
                else:
                    file_path = image_url # Attempt direct
                
                # Validate file exists
                if not os.path.exists(file_path):
                     print(f"File not found for vision analysis: {file_path}")
                     return "Image file not found for analysis."

                with open(file_path, "rb") as image_file:
                    base64_image = base64.b64encode(image_file.read()).decode('utf-8')
                    
                image_url_obj = f"data:image/jpeg;base64,{base64_image}"
            else:
                image_url_obj = image_url

            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": "Describe this fashion product in detail. Include color, pattern, material, style, and key features. Be concise but descriptive."},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": image_url_obj,
                                },
                            },
                        ],
                    }
                ],
                model=self.model,
            )
            description = chat_completion.choices[0].message.content
            return description
        except Exception as e:
            print(f"Error in Vision Service: {e}")
            return ""

vision_service = VisionService()
