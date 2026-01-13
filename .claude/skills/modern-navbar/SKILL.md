---
name: modern-navbar
description: Create stunning modern navigation bars with glassmorphism, animations, and responsive design. Use when user wants contemporary navbar designs.
---

# Modern UI Navbar Design

## Instructions
Create navigation bars with these contemporary features:

### 1. **Glassmorphism Effect**
   - Semi-transparent background with blur
   - Subtle border with gradient
   - Frosted glass appearance
   - Dynamic backdrop filter

### 2. **Smooth Animations**
   - Fade-in on scroll
   - Hover state transitions
   - Active link indicators
   - Mobile menu slide animations
   - Micro-interactions on logo and items

### 3. **Responsive Behavior**
   - Desktop: Horizontal layout with full menu
   - Tablet: Condensed spacing
   - Mobile: Hamburger menu with slide-out drawer
   - Touch-optimized tap targets (min 44px)

### 4. **Modern Design Elements**
   - Floating/sticky positioning
   - Gradient accents
   - Icon integration
   - Search bar with animation
   - Profile/avatar components
   - Notification badges

### 5. **Accessibility**
   - ARIA labels for screen readers
   - Keyboard navigation support
   - Focus indicators
   - Semantic HTML structure

## Example Code

```html
<nav class="modern-navbar">
  <div class="navbar-container">
    <a href="#" class="navbar-logo">
      <span class="logo-text">Brand</span>
    </a>
    
    <ul class="navbar-menu">
      <li><a href="#" class="nav-link active">Home</a></li>
      <li><a href="#" class="nav-link">Products</a></li>
      <li><a href="#" class="nav-link">About</a></li>
      <li><a href="#" class="nav-link">Contact</a></li>
    </ul>
    
    <button class="mobile-toggle" aria-label="Toggle menu">
      <span></span>
      <span></span>
      <span></span>
    </button>
  </div>
</nav>
```

```css
.modern-navbar {
  position: fixed;
  top: 0;
  width: 100%;
  background: rgba(255, 255, 255, 0.08);
  backdrop-filter: blur(20px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  z-index: 1000;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.navbar-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 1rem 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.navbar-logo {
  font-size: 1.5rem;
  font-weight: 700;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  transition: transform 0.3s ease;
}

.navbar-logo:hover {
  transform: scale(1.05);
}

.navbar-menu {
  display: flex;
  gap: 2rem;
  list-style: none;
  margin: 0;
  padding: 0;
}

.nav-link {
  color: rgba(255, 255, 255, 0.9);
  text-decoration: none;
  font-weight: 500;
  padding: 0.5rem 1rem;
  border-radius: 8px;
  position: relative;
  transition: all 0.3s ease;
}

.nav-link::before {
  content: '';
  position: absolute;
  bottom: 0;
  left: 50%;
  width: 0;
  height: 2px;
  background: linear-gradient(90deg, #667eea, #764ba2);
  transform: translateX(-50%);
  transition: width 0.3s ease;
}

.nav-link:hover {
  background: rgba(255, 255, 255, 0.1);
  color: #fff;
}

.nav-link:hover::before,
.nav-link.active::before {
  width: 80%;
}

.mobile-toggle {
  display: none;
  flex-direction: column;
  gap: 5px;
  background: transparent;
  border: none;
  cursor: pointer;
  padding: 0.5rem;
}

.mobile-toggle span {
  width: 25px;
  height: 2px;
  background: rgba(255, 255, 255, 0.9);
  transition: all 0.3s ease;
  border-radius: 2px;
}

/* Scrolled state */
.modern-navbar.scrolled {
  background: rgba(255, 255, 255, 0.95);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
}

.modern-navbar.scrolled .nav-link {
  color: rgba(0, 0, 0, 0.8);
}

/* Mobile Responsive */
@media (max-width: 768px) {
  .mobile-toggle {
    display: flex;
  }
  
  .navbar-menu {
    position: fixed;
    top: 0;
    right: -100%;
    height: 100vh;
    width: 70%;
    max-width: 300px;
    background: rgba(20, 20, 30, 0.98);
    backdrop-filter: blur(20px);
    flex-direction: column;
    padding: 5rem 2rem 2rem;
    transition: right 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    box-shadow: -5px 0 30px rgba(0, 0, 0, 0.3);
  }
  
  .navbar-menu.active {
    right: 0;
  }
  
  .nav-link {
    width: 100%;
    padding: 1rem;
    text-align: left;
  }
}
```

```javascript
// Navbar scroll effect
const navbar = document.querySelector('.modern-navbar');
window.addEventListener('scroll', () => {
  if (window.scrollY > 50) {
    navbar.classList.add('scrolled');
  } else {
    navbar.classList.remove('scrolled');
  }
});

// Mobile menu toggle
const mobileToggle = document.querySelector('.mobile-toggle');
const navbarMenu = document.querySelector('.navbar-menu');

mobileToggle.addEventListener('click', () => {
  navbarMenu.classList.toggle('active');
  mobileToggle.classList.toggle('active');
});
```

## Design Variations

### Dark Mode
```css
.modern-navbar.dark {
  background: rgba(20, 20, 30, 0.9);
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}
```

### Neumorphism Style
```css
.modern-navbar.neumorphic {
  background: #e0e5ec;
  box-shadow: 9px 9px 16px #a3b1c6, -9px -9px 16px #ffffff;
  border: none;
}
```

### Minimal Transparent
```css
.modern-navbar.minimal {
  background: transparent;
  backdrop-filter: none;
  border: none;
}
```

## Best Practices
- Keep navbar height between 60-80px for desktop
- Use z-index of 1000+ for fixed positioning
- Implement smooth transitions (0.3s recommended)
- Ensure mobile menu has close button or overlay
- Add active state indicators for current page
- Use semantic HTML5 `<nav>` element
- Test on multiple devices and browsers