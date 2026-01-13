## MODERN UI HERO SECTION

---
name: modern-hero
description: Create impactful hero sections with animations, gradients, and interactive elements. Use when user wants landing page hero designs.
---

### Instructions
Create hero sections with these features:

#### **Visual Impact**
- Full viewport height (100vh)
- Gradient backgrounds or video backgrounds
- Animated particles or geometric shapes
- Parallax scrolling effects
- Split-screen layouts

#### **Content Elements**
- Bold typography with gradients
- Animated headlines (typewriter, fade-in)
- Call-to-action buttons with effects
- Hero images with overlay effects
- Social proof elements (logos, stats)

#### **Animation Types**
- Fade-in on load
- Scroll-triggered animations
- Floating elements
- Gradient animations
- Mouse-following effects

### Example Code

```html
<section class="hero-section">
  <div class="hero-background">
    <div class="gradient-overlay"></div>
    <div class="particles" id="particles"></div>
  </div>
  
  <div class="hero-content">
    <div class="hero-badge">✨ New Release 2026</div>
    <h1 class="hero-title">
      Build Amazing
      <span class="gradient-text">Experiences</span>
    </h1>
    <p class="hero-subtitle">
      Create stunning websites with modern design principles and cutting-edge technology
    </p>
    <div class="hero-cta">
      <button class="btn-primary">Get Started</button>
      <button class="btn-secondary">Watch Demo</button>
    </div>
    <div class="hero-stats">
      <div class="stat-item">
        <h3>10K+</h3>
        <p>Active Users</p>
      </div>
      <div class="stat-item">
        <h3>50+</h3>
        <p>Countries</p>
      </div>
      <div class="stat-item">
        <h3>99%</h3>
        <p>Satisfaction</p>
      </div>
    </div>
  </div>
  
  <div class="hero-image">
    <img src="hero-graphic.png" alt="Hero graphic">
  </div>
  
  <div class="scroll-indicator">
    <span>Scroll Down</span>
    <div class="arrow-down"></div>
  </div>
</section>
```

```css
.hero-section {
  position: relative;
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  padding: 2rem;
}

.hero-background {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
  z-index: -1;
}

.gradient-overlay {
  position: absolute;
  width: 100%;
  height: 100%;
  background: radial-gradient(circle at 50% 50%, rgba(255,255,255,0.1) 0%, transparent 70%);
  animation: pulse 4s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 0.5; }
  50% { opacity: 1; }
}

.hero-content {
  max-width: 1200px;
  text-align: center;
  z-index: 10;
  animation: fadeInUp 1s ease-out;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.hero-badge {
  display: inline-block;
  background: rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.3);
  padding: 0.5rem 1.5rem;
  border-radius: 30px;
  color: white;
  font-weight: 600;
  margin-bottom: 2rem;
  animation: slideInDown 0.8s ease-out;
}

@keyframes slideInDown {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.hero-title {
  font-size: clamp(2.5rem, 8vw, 5rem);
  font-weight: 900;
  color: white;
  margin-bottom: 1.5rem;
  line-height: 1.2;
}

.gradient-text {
  display: block;
  background: linear-gradient(90deg, #fff, #f093fb, #fff);
  background-size: 200% auto;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  animation: gradientShift 3s ease infinite;
}

@keyframes gradientShift {
  0%, 100% { background-position: 0% center; }
  50% { background-position: 100% center; }
}

.hero-subtitle {
  font-size: clamp(1rem, 3vw, 1.5rem);
  color: rgba(255, 255, 255, 0.9);
  max-width: 600px;
  margin: 0 auto 3rem;
  line-height: 1.6;
}

.hero-cta {
  display: flex;
  gap: 1.5rem;
  justify-content: center;
  flex-wrap: wrap;
  margin-bottom: 4rem;
}

.btn-primary,
.btn-secondary {
  padding: 1rem 2.5rem;
  border-radius: 12px;
  font-size: 1.1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  border: none;
}

.btn-primary {
  background: white;
  color: #667eea;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
}

.btn-primary:hover {
  transform: translateY(-3px) scale(1.05);
  box-shadow: 0 15px 50px rgba(0, 0, 0, 0.3);
}

.btn-secondary {
  background: transparent;
  color: white;
  border: 2px solid white;
}

.btn-secondary:hover {
  background: white;
  color: #667eea;
  transform: translateY(-3px);
}

.hero-stats {
  display: flex;
  gap: 3rem;
  justify-content: center;
  flex-wrap: wrap;
}

.stat-item {
  text-align: center;
}

.stat-item h3 {
  font-size: 2.5rem;
  font-weight: 900;
  color: white;
  margin-bottom: 0.5rem;
}

.stat-item p {
  color: rgba(255, 255, 255, 0.8);
  font-size: 1rem;
}

.scroll-indicator {
  position: absolute;
  bottom: 2rem;
  left: 50%;
  transform: translateX(-50%);
  text-align: center;
  color: white;
  animation: bounce 2s infinite;
}

@keyframes bounce {
  0%, 20%, 50%, 80%, 100% { transform: translateX(-50%) translateY(0); }
  40% { transform: translateX(-50%) translateY(-10px); }
  60% { transform: translateX(-50%) translateY(-5px); }
}

.arrow-down {
  width: 20px;
  height: 20px;
  border-left: 2px solid white;
  border-bottom: 2px solid white;
  transform: rotate(-45deg);
  margin: 0.5rem auto;
}

/* Particles Effect */
.particles {
  position: absolute;
  width: 100%;
  height: 100%;
}

@media (max-width: 768px) {
  .hero-cta {
    flex-direction: column;
    align-items: center;
  }
  
  .btn-primary,
  .btn-secondary {
    width: 100%;
    max-width: 300px;
  }
}
```