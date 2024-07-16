for (let i = 0; i < 50; i++) {
    const flake = document.createElement('div');
    flake.classList.add('snowflake');

    // Random size, positions, and animation delays
    const size = (Math.random() * 0.5 + 0.2) + 'vw';
    const leftInitial = (Math.random() * 100 - 50) + 'vw';
    const leftEnd = (Math.random() * 100 - 50) + 'vw';
    const animationDuration = (Math.random() * 10 + 5) + 's';
    const animationDelay = (Math.random() * -10) + 's';

    // Applying styles to each snowflake
    flake.style.width = size;
    flake.style.height = size;
    flake.style.left = Math.random() * 100 + 'vw';
    flake.style.animationName = 'snowfall';
    flake.style.animationDuration = animationDuration;
    flake.style.animationTimingFunction = 'linear';
    flake.style.animationIterationCount = 'infinite';
    flake.style.animationDelay = animationDelay;

    // Calculating and setting the initial and end positions for the animation
    flake.style.setProperty('--left-ini', leftInitial);
    flake.style.setProperty('--left-end', leftEnd);

    // Add blur randomly for every 6 snowflakes
    if (i % 6 === 0) {
        flake.style.filter = 'blur(1px)';
    }

    document.body.appendChild(flake);
}
