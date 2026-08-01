let curedCount = 0;
let moneyEarned = 0.00;

const boredomBtn = document.getElementById('boredomBtn');
const curedScoreEl = document.getElementById('curedScore');
const moneyScoreEl = document.getElementById('moneyScore');
const modalOverlay = document.getElementById('modalOverlay');
const modalBody = document.getElementById('modalBody');

// Main click action: Cures boredom and increments simulated revenue
boredomBtn.addEventListener('click', (e) => {
    curedCount += 1;
    moneyEarned += 0.01; // Every click makes fractional ad revenue!
    
    updateStats();
    createFloatingText(e.clientX, e.clientY);
});

function updateStats() {
    curedScoreEl.textContent = curedCount.toLocaleString();
    moneyScoreEl.textContent = '$' + moneyEarned.toFixed(2);
}

// Floating click animation numbers (+1 Boredom, +$0.01)
function createFloatingText(x, y) {
    const el = document.createElement('div');
    el.textContent = '+1 🎉';
    el.style.position = 'fixed';
    el.style.left = (x - 20 + Math.random() * 40) + 'px';
    el.style.top = (y - 20) + 'px';
    el.style.color = '#facc15';
    el.style.fontWeight = 'bold';
    el.style.fontSize = '14px';
    el.style.pointerEvents = 'none';
    el.style.zIndex = '9999';
    el.style.transition = 'transform 0.6s ease, opacity 0.6s ease';
    
    document.body.appendChild(el);
    
    setTimeout(() => {
        el.style.transform = 'translateY(-50px)';
        el.style.opacity = '0';
    }, 20);
    
    setTimeout(() => {
        el.remove();
    }, 600);
}

// Fake Ad Interactivity
function fakeAdClick(e) {
    e.preventDefault();
    alert("🎉 CONGRATULATIONS! You clicked a high-CPM advertisement! Estimated advertiser payout recorded ($0.05 added to ledger).");
    moneyEarned += 0.05;
    updateStats();
}

function toggleAds(e) {
    e.preventDefault();
    alert("Nice try! Ad-blocker detected. Premium ad-free subscription costs $99.99/mo. Returning you to free ad-supported mode.");
}

// Mini Game Modal Trigger
function triggerPopup(type) {
    modalOverlay.style.display = 'flex';
    
    if (type === 'reaction') {
        modalBody.innerHTML = `
            <h3 style="color:var(--accent-cyan); margin-bottom:10px;">⚡ Quick Reaction Test</h3>
            <p style="font-size:12px; color:var(--text-muted); margin-bottom:15px;">Click the target as fast as you can when it turns green!</p>
            <div id="reactionBox" style="background:#1f293d; height:100px; border-radius:8px; display:flex; align-items:center; justify-content:center; cursor:pointer; font-weight:bold; color:#cbd5e1;" onclick="handleReactionClick()">
                Click to Start
            </div>
        `;
    } else if (type === 'fortune') {
        const fortunes = [
            "You will accidentally invent a sandwich that tastes like colors.",
            "A raccoon will look at you with deep respect this week.",
            "Your Wi-Fi will drop precisely 3 seconds before an important moment.",
            "You are destined to click at least 500 more banner ads today."
        ];
        const randomFortune = fortunes[Math.floor(Math.random() * fortunes.length)];
        modalBody.innerHTML = `
            <h3 style="color:var(--accent-yellow); margin-bottom:10px;">🔮 The Boredom Oracle</h3>
            <p style="font-size:14px; color:white; margin:20px 0; font-style:italic;">"${randomFortune}"</p>
            <button class="ad-btn" onclick="closeModal()">Accept Fate</button>
        `;
    } else if (type === 'popup') {
        modalBody.innerHTML = `
            <h3 style="color:var(--accent-pink); margin-bottom:10px;">🎁 YOU ARE VISITOR #1,000,000!</h3>
            <p style="font-size:12px; color:var(--text-muted); margin-bottom:15px;">Claim your free Brand New Phone right now by clicking below!</p>
            <button class="ad-btn" style="background:var(--accent-yellow); color:#000;" onclick="fakeAdClick(event)">CLAIM REWARD</button>
        `;
    }
}

let reactionState = 'waiting';
let startTime = 0;

function handleReactionClick() {
    const box = document.getElementById('reactionBox');
    if (reactionState === 'waiting') {
        box.style.background = '#dc2626';
        box.textContent = 'Wait for Green...';
        reactionState = 'ready';
        
        setTimeout(() => {
            if (reactionState === 'ready') {
                box.style.background = '#16a34a';
                box.textContent = 'CLICK NOW!!';
                box.style.color = 'white';
                startTime = Date.now();
                reactionState = 'click';
            }
        }, 1000 + Math.random() * 2000);
    } else if (reactionState === 'ready') {
        box.style.background = '#dc2626';
        box.textContent = 'Too soon! Click to restart.';
        reactionState = 'waiting';
    } else if (reactionState === 'click') {
        const elapsed = Date.now() - startTime;
        box.style.background = '#1f293d';
        box.textContent = `Your time: ${elapsed}ms! Bonus $0.10 earned!`;
        moneyEarned += 0.10;
        updateStats();
        reactionState = 'waiting';
    }
}

function closeModal() {
    modalOverlay.style.display = 'none';
    reactionState = 'waiting';
}

modalOverlay.addEventListener('click', (e) => {
    if (e.target === modalOverlay) closeModal();
});

// Passive background ticker to make simulated ad revenue grow naturally
setInterval(() => {
    if (Math.random() > 0.4) {
        moneyEarned += 0.005;
        updateStats();
    }
-}, 2500);
