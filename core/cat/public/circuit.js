var paths = document.querySelectorAll('.st0');

function animatePath(path, reveal) {
  var length = path.getTotalLength();
  var randomDelay = Math.random() * 20 ;
  
  path.style.transition = path.style.WebkitTransition = 'stroke-dashoffset ' + randomDelay + 's ease-in-out';
    path.style.strokeDasharray = length + ' ' + length;
  if (reveal) {
    path.style.strokeDashoffset = '0';
  } else {
    path.style.strokeDashoffset = length;
  }
  
  setTimeout(function() {
    if (reveal) {
      path.style.strokeDashoffset = length;
    } else {
      path.style.strokeDashoffset = '0';
    }

    setTimeout(function() {
      animatePath(path, !reveal); // Toggle between reveal and reverse
    }, randomDelay * 1000); // Convert to milliseconds

  }, randomDelay * 1000); // Convert to milliseconds
}

[].forEach.call(paths, function(path) {
  animatePath(path, true); // Start with reveal animation
});