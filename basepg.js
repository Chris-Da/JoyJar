
  const testimonials = [
    {
      text: "“This website is an incredible source of knowledge and comfort for me. I'm going through one of the hardest times of my life mentally, and you have made me feel less alone.”",
      author: "— From Canada"
    },
    {
      text: "“JoyJar helped me understand my anxiety and showed me healthy ways to cope. It made a huge difference in my daily life.”",
      author: "— From South Africa"
    },
    {
      text: "“I found JoyJar during a really tough time, and its calming meditations and advice felt like a warm hug.”",
      author: "— From Australia"
    },
    {
      text: "“The tips here helped my teenage son through depression. We finally felt seen and supported.”",
      author: "— From United States"
    }
  ];

  const display = document.getElementById("testimonial-display");
  const left = document.querySelector(".testimonial-arrow.left");
  const right = document.querySelector(".testimonial-arrow.right");
  let index = 0;

  function showTestimonial(i) {
    display.querySelector("p").textContent = testimonials[i].text;
    display.querySelector("span").textContent = testimonials[i].author;
  }

  left.addEventListener("click", () => {
    index = (index - 1 + testimonials.length) % testimonials.length;
    showTestimonial(index);
  });

  right.addEventListener("click", () => {
    index = (index + 1) % testimonials.length;
    showTestimonial(index);
  });
