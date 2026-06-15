// ========== Mobile Menu Toggle ==========
const menuToggle = document.getElementById('menuToggle');
const navLinks = document.getElementById('navLinks');

if (menuToggle) {
    menuToggle.addEventListener('click', () => {
        navLinks.classList.toggle('active');
    });

    // Close menu when clicking on a link
    document.querySelectorAll('.nav-links a').forEach(link => {
        link.addEventListener('click', () => {
            navLinks.classList.remove('active');
        });
    });
}

// ========== Contact Form Handling ==========
const contactForm = document.getElementById('contactForm');
if (contactForm) {
    const formMessage = document.getElementById('formMessage');

    contactForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        // Get form data
        const formData = {
            name: document.getElementById('name').value,
            email: document.getElementById('email').value,
            phone: document.getElementById('phone').value || '',
            service: document.getElementById('service').value,
            message: document.getElementById('message').value
        };

        // Validate form
        if (!formData.name || !formData.email || !formData.service || !formData.message) {
            showMessage('Please fill in all required fields', false);
            return;
        }

        // Validate email
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(formData.email)) {
            showMessage('Please enter a valid email address', false);
            return;
        }

        try {
            // Send to Flask backend
            const response = await fetch('/api/submit-message', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(formData)
            });

            const data = await response.json();

            if (data.success) {
                showMessage('✓ ' + data.message, true);
                contactForm.reset();

                // Hide message after 5 seconds
                setTimeout(() => {
                    formMessage.classList.remove('success');
                    formMessage.textContent = '';
                }, 5000);
            } else {
                showMessage('✗ ' + (data.error || 'Something went wrong'), false);
            }
        } catch (error) {
            showMessage('✗ Network error. Please try again.', false);
            console.error('Form submission error:', error);
        }
    });

    // Helper function to show messages
    function showMessage(message, isSuccess) {
        formMessage.textContent = message;
        formMessage.classList.toggle('success', isSuccess);
    }
}

// ========== Smooth Scroll Enhancement ==========
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        const href = this.getAttribute('href');
        if (href !== '#' && document.querySelector(href)) {
            e.preventDefault();
            document.querySelector(href).scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// ========== Intersection Observer for Animations ==========
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -100px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, observerOptions);

// Observe service cards and features
document.querySelectorAll('.service-card, .feature').forEach(element => {
    element.style.opacity = '0';
    element.style.transform = 'translateY(20px)';
    element.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
    observer.observe(element);
});

// ========== Active Navigation Link ==========
const navItems = document.querySelectorAll('.nav-links a');
window.addEventListener('scroll', () => {
    let current = '';
    document.querySelectorAll('section').forEach(section => {
        const sectionTop = section.offsetTop;
        if (pageYOffset >= sectionTop - 200) {
            current = section.getAttribute('id');
        }
    });

    navItems.forEach(item => {
        item.style.color = '';
        if (item.getAttribute('href') === '#' + current) {
            item.style.color = 'var(--primary-color)';
        }
    });
});

// ========== Log Initialize ==========
console.log('TechFix Pro Website - Loaded Successfully ✓');