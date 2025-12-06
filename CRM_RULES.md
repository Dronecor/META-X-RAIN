# Fashion Retail CRM - System Rules & Guidelines

## 🎯 Core Mission
Build lasting customer relationships through personalized, multi-channel fashion retail experiences combining chat, catalog images, and smart recommendations.

---

## 1. CUSTOMER RELATIONSHIP PIPELINE

### Customer Journey Stages
```
Lead → Interested → Engaged → Customer → Repeat → Loyal
```

### Customer Profile Tracking
Every customer record includes:
- **Identity**: Name, phone, email
- **Interaction History**: 
  - All chat conversations (WhatsApp / Email / Website)
  - Orders & payment history
  - Images viewed, liked, or purchased
- **Preferences**: 
  - Style preferences
  - Size information
  - Favorite categories
  - Budget range
- **Engagement Metrics**:
  - Last interaction date
  - Assigned sales representative
  - Customer segment (VIP, one-time, window shopper, repeat)

### Automatic Segmentation
- **VIP**: High-value repeat customers (3+ orders, $500+ total)
- **Repeat Buyers**: 2+ orders
- **One-Time Buyers**: 1 order, no recent activity
- **Window Shoppers**: Engaged but no purchases
- **Inactive Leads**: No interaction in 30+ days

### Follow-Up System
- Generate reminders for inactive leads (30 days)
- Notify about new catalog items matching preferences
- Birthday/anniversary messages for VIP customers

---

## 2. MESSAGE & RESPONSE RULES

### Length Guidelines
| Message Type | Max Length | Structure |
|-------------|-----------|-----------|
| Auto Messages | 12-25 words | Single sentence |
| Sales Replies | 2-4 lines | Greeting + Info + Question |
| Support Replies | 2-4 lines | Acknowledge + Solution + Next Step |
| Promotions | 3 lines | Hook → Offer → CTA |

### Tone Requirements
✅ **DO:**
- Sound natural and conversational
- Be friendly and approachable
- Use emojis sparingly (✨, 👗, 💫, 💙)
- Ask clarifying questions when needed
- End with clear next steps

❌ **DON'T:**
- Use formal business language
- Write long paragraphs
- Repeat information unnecessarily
- Sound robotic or scripted

### Example Messages

**Good Auto Message:**
"Hi Sarah! 👋 Your order #1234 shipped today. Track it here: [link]"

**Good Sales Reply:**
"Love your style! 💫 
For that wedding, I'd suggest our navy midi dress ($159) or the classic black evening gown ($189).
Want to see them?"

**Good Promotion:**
"Flash Sale Alert! ✨
Get 25% off all summer dresses today only.
Shop now → [link]"

---

## 3. IMAGE HANDLING RULES

### Display Format
- **Grid View**: 2-3 products per row for browsing
- **Carousel View**: Multiple angles for single product
- **Chat Embedded**: Images inline with text responses

### Image Metadata (Required)
```json
{
  "product_id": "DRESS-001",
  "name": "Navy Midi Dress",
  "category": "Dresses",
  "tags": ["elegant", "wedding", "formal"],
  "price": 159.00,
  "stock_status": "in_stock",
  "image_url": "https://...",
  "sizes_available": ["S", "M", "L"]
}
```

### AI-Based Search
Match customer queries to:
- Product tags (e.g., "elegant", "casual", "summer")
- Categories (dresses, shoes, accessories)
- Occasions (wedding, work, party)
- Colors and patterns
- Price ranges

### Image Response Format
```
![Product Name](image_url)
Product Name - $Price ✓ In Stock
[Quick Add] [View Details]
```

---

## 4. AI RECOMMENDATION ENGINE

### Recommendation Factors
1. **Purchase History**: Items previously bought
2. **Browsing Behavior**: Viewed/liked products
3. **Style Profile**: Preferred categories, colors, styles
4. **Contextual**: Current season, trending items
5. **Inventory**: Prioritize in-stock items

### Personalization Rules
- Match customer's size preferences
- Respect budget constraints
- Suggest complementary items (complete the outfit)
- Reference past purchases: "This would pair perfectly with the dress you bought last month!"

### Example Recommendation Flow
```
Customer: "I need shoes for a summer wedding"

AI Analysis:
- Previous purchase: Navy midi dress
- Style: Elegant, classic
- Budget: Mid-range ($100-200)

Recommendation:
"Perfect! Since you have that beautiful navy dress, I'd suggest:
1. Nude strappy heels ($129) - elongates legs
2. Gold block heels ($145) - comfortable & elegant
Want to see them?"
```

---

## 5. SYSTEM OUTPUT FORMAT

### Chat Response Structure
```
[Greeting/Acknowledgment]
[Main Content: Text + Images]
[Call-to-Action / Next Step]
```

### Quick Action Buttons
- 🛒 Add to Cart
- 👀 View Details
- 💬 Chat with Sales Rep
- 📦 Track Order
- 🔄 Request Exchange

### Multi-Image Response Example
```
Here are your top matches! ✨

![Dress 1](url1)
Navy Midi Dress - $159 ✓ In Stock
[Add to Cart]

![Dress 2](url2)
Black Evening Gown - $189 ✓ In Stock
[Add to Cart]

Which style speaks to you? I can also suggest accessories! 💫
```

---

## 6. MULTI-CHANNEL INTEGRATION

### Unified Customer Timeline
All interactions from these channels merge into one history:
- WhatsApp messages
- Email conversations
- Website chat
- Phone calls (logged by sales reps)
- In-store visits (if tracked)

### Context Retrieval
Before responding, AI must:
1. Load customer profile
2. Review last 10 interactions
3. Check current conversation summary
4. Identify customer segment
5. Retrieve relevant product history

### Channel-Specific Formatting
- **WhatsApp**: Shorter, emoji-friendly
- **Email**: Slightly more formal, can be longer
- **Website Chat**: Real-time, conversational

---

## 7. OPERATIONAL RULES

### Clarification Protocol
If customer request is ambiguous:
```
"Just to make sure I get this right - are you looking for [option A] or [option B]? 😊"
```

### Logging Requirements
Every interaction must log:
- Timestamp
- Channel (WhatsApp/Email/Web)
- Customer ID
- Agent (AI or Human)
- Message content
- Products mentioned/shown
- Actions taken (added to cart, order placed, etc.)

### Product Repetition
- Don't show the same product twice unless:
  - Customer explicitly asks again
  - Different context (e.g., showing with different outfit)
  - New stock/price update

### Response Speed
- Auto-replies: Instant
- AI responses: < 2 seconds
- Human handoff: < 5 minutes during business hours

---

## 8. ANALYTICS & INSIGHTS

### Track These Metrics
- Conversation → Purchase conversion rate
- Average response time
- Customer satisfaction scores
- Product view → Add to cart rate
- Repeat customer rate by segment
- Most recommended products
- Peak conversation times

### Weekly Reports
- New leads vs. conversions
- VIP customer activity
- Inactive customers needing follow-up
- Top-selling products via chat
- Common support issues

---

## 🎯 SUCCESS CRITERIA

A successful interaction includes:
✅ Customer feels heard and valued
✅ Response is relevant and personalized
✅ Clear next step provided
✅ Product recommendations match preferences
✅ Images enhance (not replace) conversation
✅ Tone is natural and friendly
✅ All data logged for future reference

---

## 🚫 WHAT TO AVOID

❌ Generic, copy-paste responses
❌ Overwhelming with too many options (max 3 products at once)
❌ Ignoring customer history
❌ Being pushy or sales-aggressive
❌ Long, formal messages
❌ Showing out-of-stock items without mentioning it
❌ Forgetting to ask follow-up questions

---

**Remember**: This is not just a chatbot - it's a relationship-building system. Every interaction should move the customer forward in their journey while making them feel valued and understood.
