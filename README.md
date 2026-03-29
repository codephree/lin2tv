# Link 2 TV

A beautiful, modern frontend for a link to Television service using Tailwind CSS and jQuery. Users can submit a link to generate a code, and retrieve the original link using the code. Includes a copy-to-clipboard feature for convenience.

## Features
- Responsive, glassmorphism UI with Tailwind CSS
- Submit a link to generate a short code
- Retrieve a link from a code
- Copy-to-clipboard button for easy sharing
- jQuery-powered AJAX for seamless UX

## Getting Started

1. **Clone the repository**
2. **Build and run with Docker**
   ```sh
   docker build -t link-2-tv .
   docker run -p 5000:5000 link-2-tv
   ```
   The app will be available at http://localhost:5000
3. **Configure AJAX endpoints**
   - The frontend is preconfigured to use `/api/generate` and `/api/retrieve` which are handled by the backend.

## Requirements
- [Tailwind CSS CDN](https://cdn.tailwindcss.com/)
- [jQuery CDN](https://code.jquery.com/)
- A backend API for generating and retrieving links

## Customization
- Edit the HTML and Tailwind classes in `index.html` to further style or extend functionality.

## License
MIT
