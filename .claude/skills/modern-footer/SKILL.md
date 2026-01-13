## MODERN UI FOOTER DESIGN

---
name: modern-footer
description: Create comprehensive footer sections with links, social media, and newsletter signup. Use when user wants footer designs.
---

### Instructions
Create footer sections with these features:

#### **Layout Structure**
- Multi-column layouts (3-5 columns)
- Newsletter subscription form
- Social media icons
- Contact information
- Sitemap links
- Logo and brand info

#### **Visual Design**
- Dark or light themes
- Gradient backgrounds
- Divider lines
- Hover effects on links
- Icon animations

#### **Content Sections**
- Company info
- Product/service links
- Resources and support
- Legal links (privacy, terms)
- Contact details
- Payment methods/badges

### Example Code

```html
<footer class="modern-footer">
  <div class="footer-content">
    <div class="footer-section">
      <div class="footer-logo">
        <h2>Brand</h2>
        <p>Creating amazing digital experiences since 2020</p>
      </div>
      <div class="social-links">
        <a href="#" class="social-icon">
          <svg><!-- Twitter icon --></svg>
        </a>
        <a href="#" class="social-icon">
          <svg><!-- LinkedIn icon --></svg>
        </a>
        <a href="#" class="social-icon">
          <svg><!-- GitHub icon --></svg>
        </a>
      </div>
    </div>
    
    <div class="footer-section">
      <h3>Products</h3>
      <ul class="footer-links">
        <li><a href="#">Features</a></li>
        <li><a href="#">Pricing</a></li>
        <li><a href="#">Enterprise</a></li>
        <li><a href="#">API</a></li>
      </ul>
    </div>
    
    <div class="footer-section">
      <h3>Resources</h3>
      <ul class="footer-links">
        <li><a href="#">Documentation</a></li>
        <li><a href="#">Tutorials</a></li>
        <li><a href="#">Blog</a></li>
        <li><a href="#">Support</a></li>
      </ul>
    </div>
    
    <div class="footer-section">
      <h3>Newsletter</h3>
      <p>Subscribe to get updates</p>
      <form class="newsletter-form">
        <input type="email" placeholder="Enter your email">
        <button type="submit">Subscribe</button>
      </form>
    </div>
  </div>
  
  <div class="footer-bottom">
    <p>&copy; 2026 Brand. All rights reserved.</p>
    <div class="footer-legal">
      <a href="#">Privacy Policy</a>
      <a href="#">Terms of Service</a>
      <a href="#">Cookie Policy</a>
    </div>
  </div>
</footer>
```

```css
.modern-footer {
  background: linear-gradient(135deg, #1e1e2e 0%, #2d2d44 100%);
  color: rgba(255, 255, 255, 0.9);
  padding: 4rem 2rem 2rem;
  position: relative;
  overflow: hidden;
}

.modern-footer::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
}

.footer-content {
  max-width: 1200px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 3rem;
  margin-bottom: 3rem;
}

.footer-section h3 {
  font-size: 1.2rem;
  font-weight: 700;
  margin-bottom: 1.5rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.footer-logo h2 {
  font-size: 2rem;
  font-weight: 900;
  margin-bottom: 1rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.footer-logo p {
  color: rgba(255, 255, 255, 0.7);
  line-height: 1.6;
  margin-bottom: 1.5rem;
}

.social-links {
  display: flex;
  gap: 1rem;
}

.social-icon {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 10px;
  color: white;
  transition: all 0.3s ease;
}

.social-icon:hover {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  transform: translateY(-3px) scale(1.1);
  box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4);
}

.footer-links {
  list-style: none;
  padding: 0;
  margin: 0;
}

.footer-links li {
  margin-bottom: 0.75rem;
}

.footer-links a {
  color: rgba(255, 255, 255, 0.7);
  text-decoration: none;
  transition: all 0.3s ease;
  display: inline-block;
  position: relative;
}

.footer-links a::before {
  content: '→';
  position: absolute;
  left: -20px;
  opacity: 0;
  transition: all 0.3s ease;
}

.footer-links a:hover {
  color: white;
  padding-left: 20px;
}

.footer-links a:hover::before {
  opacity: 1;
  left: 0;
}

.newsletter-form {
  display: flex;
  gap: 0.5rem;
  margin-top: 1rem;
}

.newsletter-form input {
  flex: 1;
  padding: 0.75rem 1rem;
  border-radius: 10px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  color: white;
  transition: all 0.3s ease;
}

.newsletter-form input:focus {
  outline: none;
  border-color: #667eea;
  background: rgba(255, 255, 255, 0.15);
}

.newsletter-form button {
  padding: 0.75rem 1.5rem;
  border-radius: 10px;
  border: none;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.newsletter-form button:hover {
  transform: scale(1.05);
  box-shadow: 0 5px 20px rgba(102, 126, 234, 0.4);
}

.footer-bottom {
  max-width: 1200px;
  margin: 0 auto;
  padding-top: 2rem;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 1rem;
}

.footer-legal {
  display: flex;
  gap: 2rem;
}

.footer-legal a {
  color: rgba(255, 255, 255, 0.6);
  text-decoration: none;
  font-size: 0.9rem;
  transition: color 0.3s ease;
}

.footer-legal a:hover {
  color: white;
}

@media (max-width: 768px) {
  .footer-content {
    grid-template-columns: 1fr;
    gap: 2rem;
  }
  
  .footer-bottom {
    flex-direction: column;
    text-align: center;
  }
  
  .newsletter-form {
    flex-direction: column;
  }
}
```