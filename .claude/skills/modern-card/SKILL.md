## MODERN UI CARD DESIGNS

---
name: modern-cards
description: Create stunning card components with glassmorphism, hover effects, and modern layouts. Use when user wants contemporary card designs.
---

### Instructions
Create card components with these features:

#### **Visual Design**
- Glassmorphism with semi-transparent backgrounds
- Subtle shadows and depth
- Gradient accents and borders
- Image overlays with smooth transitions
- Icon integration

#### **Interactive Elements**
- Hover animations (lift, tilt, scale)
- Smooth transitions on all interactions
- Click/tap feedback
- Loading states
- Badge notifications

#### **Layout Options**
- Grid layouts (2, 3, 4 column)
- Masonry style
- Horizontal scrolling cards
- Stacked cards
- Flip cards (3D rotation)

#### **Card Types**
- Product cards with pricing
- Profile/team cards
- Blog post cards
- Pricing cards
- Feature cards
- Testimonial cards

### Example Code

```html
<div class="card-container">
  <div class="modern-card">
    <div class="card-image">
      <img src="image.jpg" alt="Card image">
      <div class="card-badge">New</div>
    </div>
    <div class="card-content">
      <h3 class="card-title">Card Title</h3>
      <p class="card-description">Beautiful card description with modern design elements.</p>
      <div class="card-footer">
        <span class="card-price">$99</span>
        <button class="card-button">Learn More</button>
      </div>
    </div>
  </div>
</div>
```

```css
.modern-card {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(20px);
  border-radius: 20px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  overflow: hidden;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}

.modern-card:hover {
  transform: translateY(-10px) scale(1.02);
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  border-color: rgba(255, 255, 255, 0.4);
}

.card-image {
  position: relative;
  width: 100%;
  height: 200px;
  overflow: hidden;
}

.card-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.6s ease;
}

.modern-card:hover .card-image img {
  transform: scale(1.1);
}

.card-badge {
  position: absolute;
  top: 15px;
  right: 15px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 5px 15px;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 600;
}

.card-content {
  padding: 1.5rem;
}

.card-title {
  font-size: 1.5rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.card-description {
  color: rgba(255, 255, 255, 0.8);
  margin-bottom: 1.5rem;
  line-height: 1.6;
}

.card-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-price {
  font-size: 1.5rem;
  font-weight: 700;
  color: #667eea;
}

.card-button {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 10px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.3s ease;
}

.card-button:hover {
  transform: scale(1.05);
  box-shadow: 0 5px 20px rgba(102, 126, 234, 0.4);
}

/* Flip Card Variant */
.flip-card {
  perspective: 1000px;
  height: 400px;
}

.flip-card-inner {
  position: relative;
  width: 100%;
  height: 100%;
  transition: transform 0.8s;
  transform-style: preserve-3d;
}

.flip-card:hover .flip-card-inner {
  transform: rotateY(180deg);
}

.flip-card-front,
.flip-card-back {
  position: absolute;
  width: 100%;
  height: 100%;
  backface-visibility: hidden;
  border-radius: 20px;
}

.flip-card-back {
  transform: rotateY(180deg);
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

/* Grid Layout */
.card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
  padding: 2rem;
}

@media (max-width: 768px) {
  .card-grid {
    grid-template-columns: 1fr;
    gap: 1.5rem;
  }
}
```

---