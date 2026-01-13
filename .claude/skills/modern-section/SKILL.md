## MODERN UI SECTION DESIGNS

---
name: modern-sections
description: Create engaging content sections with various layouts and animations. Use when user wants feature sections, testimonials, or content blocks.
---

### Instructions
Create content sections with these features:

#### **Section Types**
- Feature sections (grid/list)
- Testimonial carousels
- Pricing tables
- Team member grids
- FAQ accordions
- Stats/metrics sections
- CTA (Call-to-Action) sections
- Image galleries

#### **Layout Patterns**
- Alternating left/right content
- Grid layouts (2, 3, 4 columns)
- Full-width backgrounds
- Split-screen designs
- Overlapping elements
- Sticky sections

#### **Visual Effects**
- Scroll-triggered animations
- Parallax backgrounds
- Gradient overlays
- Shape dividers
- Animated counters
- Progress indicators

### Example Code

```html
<!-- Feature Section -->
<section class="feature-section">
  <div class="section-container">
    <div class="section-header">
      <span class="section-badge">Features</span>
      <h2 class="section-title">Everything You Need</h2>
      <p class="section-subtitle">Powerful features to help you build amazing products</p>
    </div>
    
    <div class="features-grid">
      <div class="feature-card">
        <div class="feature-icon">🚀</div>
        <h3>Lightning Fast</h3>
        <p>Optimized for performance and speed</p>
      </div>
      <div class="feature-card">
        <div class="feature-icon">🔒</div>
        <h3>Secure</h3>
        <p>Enterprise-grade security measures</p>
      </div>
      <div class="feature-card">
        <div class="feature-icon">📱</div>
        <h3>Responsive</h3>
        <p>Works perfectly on all devices</p>
      </div>
      <div class="feature-card">
        <div class="feature-icon">⚡</div>
        <h3>Scalable</h3>
        <p>Grows with your business needs</p>
      </div>
    </div>
  </div>
</section>

<!-- Testimonial Section -->
<section class="testimonial-section">
  <div class="section-container">
    <h2 class="section-title">What Our Clients Say</h2>
    <div class="testimonial-grid">
      <div class="testimonial-card">
        <div class="stars">⭐⭐⭐⭐⭐</div>
        <p class="testimonial-text">"This product has transformed our workflow completely. Highly recommended!"</p>
        <div class="testimonial-author">
          <img src="avatar.jpg" alt="Author">
          <div>
            <h4>John Doe</h4>
            <p>CEO, Company Inc</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>

<!-- CTA Section -->
<section class="cta-section">
  <div class="cta-content">
    <h2>Ready to Get Started?</h2>
    <p>Join thousands of satisfied customers today</p>
    <button class="cta-button">Start Free Trial</button>
  </div>
</section>
```

```css
/* Feature Section */
.feature-section {
  padding: 6rem 2rem;
  background: linear-gradient(180deg, #f8f9fa 0%, #ffffff 100%);
}

.section-container {
  max-width: 1200px;
  margin: 0 auto;
}

.section-header {
  text-align: center;
  margin-bottom: 4rem;
}

.section-badge {
  display: inline-block;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 0.5rem 1.5rem;
  border-radius: 30px;
  font-weight: 600;
  font-size: 0.9rem;
  margin-bottom: 1rem;
}

.section-title {
  font-size: clamp(2rem, 5vw, 3rem);
  font-weight: 900;
  color: #1e1e2e;
  margin-bottom: 1rem;
}

.section-subtitle {
  font-size: 1.2rem;
  color: #666;
  max-width: 600px;
  margin: 0 auto;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
}

.feature-card {
  background: white;
  padding: 2rem;
  border-radius: 20px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.05);
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  border: 1px solid rgba(0, 0, 0, 0.05);
}

.feature-card:hover {
  transform: translateY(-10px);
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.15);
  border-color: rgba(102, 126, 234, 0.3);
}

.feature-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
  display: inline-block;
  animation: float 3s ease-in-out infinite;
}

@keyframes float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
}

.feature-card h3 {
  font-size: 1.5rem;
  font-weight: 700;
  margin-bottom: 0.75rem;
  color: #1e1e2e;
}

.feature-card p {
  color: #666;
  line-height: 1.6;
}

/* Testimonial Section */
.testimonial-section {
  padding: 6rem 2rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.testimonial-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
  margin-top: 3rem;
}

.testimonial-card {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  padding: 2rem;
  border-radius: 20px;
  transition: all 0.3s ease;
}

.testimonial-card:hover {
  background: rgba(255, 255, 255, 0.15);
  transform: scale(1.02);
}

.stars {
  font-size: 1.2rem;
  margin-bottom: 1rem;
}

.testimonial-text {
  font-size: 1.1rem;
  line-height: 1.8;
  margin-bottom: 1.5rem;
  font-style: italic;
}

.testimonial-author {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.testimonial-author img {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  border: 2px solid white;
}```