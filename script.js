document.addEventListener('DOMContentLoaded', function () {
    if (localStorage.getItem('darkMode') === 'enabled') {
        document.body.classList.add('dark-mode');
    }
});

function toggleDarkMode() {
    document.body.classList.toggle('dark-mode');

    if (document.body.classList.contains('dark-mode')) {
        localStorage.setItem('darkMode', 'enabled');
        } else {
        localStorage.removeItem('darkMode');
    }
}

document.querySelector('.scroll-top-btn').addEventListener('click', function(e) {
        e.preventDefault();
        window.scrollTo({
          top: 0,
          behavior: 'smooth' 
        });
      });


function toggleMenu() {
  document.querySelector('.menu-wrapper').classList.toggle('active');
}

document.querySelectorAll('.dropdown').forEach(dropdown => {
    dropdown.addEventListener('mouseenter', () => {
      dropdown.querySelector('.dropdown-content').style.display = 'block';
    });

    dropdown.addEventListener('mouseleave', () => {
      dropdown.querySelector('.dropdown-content').style.display = 'none';
    });
  });


// document.querySelectorAll('.dropdown-submenu > a').forEach(item => {
//   item.addEventListener('click', function(e) {
//     if (window.innerWidth < 768) { // Mobile only
//       e.preventDefault();
//       this.nextElementSibling.classList.toggle('show');
//     }
//   });
// });

const circle = document.querySelector('.circle');
const audio = document.getElementById('breathing-audio');
const instructions = document.querySelector('.instructions');
const soundToggle = document.getElementById('sound-toggle');
let isPlaying = false;

document.getElementById('start-btn').addEventListener('click', function() {
  isPlaying = !isPlaying;
  if (isPlaying) {
    circle.style.animation = 'breathe 8s infinite ease-in-out';
    audio.play();
    instructions.textContent = "Breathe in... (4 sec)";
    setTimeout(() => instructions.textContent = "Hold... (4 sec)", 4000);
    setTimeout(() => instructions.textContent = "Breathe out... (4 sec)", 8000);
    this.textContent = 'Pause';
  } else {
    circle.style.animationPlayState = 'paused';
    audio.pause();
    this.textContent = 'Resume';
  }
});

soundToggle.addEventListener('click', () => {
  audio.muted = !audio.muted;
  soundToggle.textContent = audio.muted ? "🔇 Sound Off" : "🔊 Sound On";
});



const pieces = document.querySelectorAll('.puzzle-piece');

pieces.forEach(piece => {
  piece.addEventListener('dragstart', dragStart);
  piece.addEventListener('dragover', dragOver);
  piece.addEventListener('dragenter', dragEnter);
  piece.addEventListener('dragleave', dragLeave);
  piece.addEventListener('drop', dragDrop);
  piece.addEventListener('dragend', dragEnd);
});

let draggedPiece = null;

function dragStart(e) {
  draggedPiece = this;
  setTimeout(() => {
    this.classList.add('dragging');
  }, 0);
}

function dragEnd(e) {
  draggedPiece.classList.remove('dragging');
  draggedPiece = null;
}

function dragOver(e) {
  e.preventDefault();
}

function dragEnter(e) {
  this.classList.add('hovered');
}

function dragLeave(e) {
  this.classList.remove('hovered');
}

function dragDrop(e) {
  e.preventDefault();
  if (this !== draggedPiece) {
    let tempId = this.dataset.id;
    this.dataset.id = draggedPiece.dataset.id;
    draggedPiece.dataset.id = tempId;
    
    let tempBg = this.style.backgroundImage;
    this.style.backgroundImage = draggedPiece.style.backgroundImage;
    draggedPiece.style.backgroundImage = tempBg;
  }
  this.classList.remove('hovered');
}
