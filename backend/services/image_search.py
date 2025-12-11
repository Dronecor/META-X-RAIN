from typing import List, Dict, Any

class ImageSearchService:
    def __init__(self):
        # Load CLIP model or similar here
        # self.model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
        pass

    def get_image_embedding(self, image_url: str) -> List[float]:
        """
        Downloads image and generates embedding using a vision model.
        """
        print(f"[MOCK] Generated embedding for image: {image_url}")
        return [0.05] * 512 # Mock CLIP embedding

    async def search_by_image(self, image_url: str) -> List[Dict[str, Any]]:
        """
        1. Analyzes user image to get a description.
        2. Fetches products from DB.
        3. [Simple Match] Filters products by basic keyword overlap (naive).
        * In production, use Vector Search (Pinecone) or an LLM Agent to rank these candidates.
        """
        from backend.services.vision_service import vision_service
        from backend.database import SessionLocal
        from backend.models import Product
        
        # 1. Analyze User Image
        print(f"Generating description for user image: {image_url}")
        user_image_desc = vision_service.analyze_image(image_url)
        print(f"User Image Description: {user_image_desc}")
        
        db = SessionLocal()
        try:
            # 2. Get All Available Products
            products = db.query(Product).filter(Product.is_available == True).limit(50).all()
            
            if not products:
                return []

            # 3. Simple Keyword Ranking (Naive implementation to demonstrate flow)
            # We count how many words from user desc overlap with product desc
            scored_products = []
            user_words = set(user_image_desc.lower().split())
            
            for p in products:
                if not p.visual_description:
                    continue
                    
                prod_words = set(p.visual_description.lower().split())
                overlap = len(user_words.intersection(prod_words))
                
                # Boost if category matches (extracted from desc logic, simplified here)
                scored_products.append((p, overlap))
            
            # Sort by overlap score
            scored_products.sort(key=lambda x: x[1], reverse=True)
            
            # Return top 5
            top_products = [p for p, score in scored_products[:5]]
            
            # Fallback if no text match found (to ensure we always show something)
            if not top_products and products:
                top_products = products[:3]

            results = []
            for p in top_products:
                results.append({
                    "id": p.id,
                    "name": p.name,
                    "price": p.price, # Naira symbol handled in frontend usually
                    "visual_description": p.visual_description,
                    "image_url": p.image_url or "https://via.placeholder.com/150"
                })
                
            return results
        except Exception as e:
            print(f"Error in semantic image search: {e}")
            return []
        finally:
            db.close()

image_search_service = ImageSearchService()
