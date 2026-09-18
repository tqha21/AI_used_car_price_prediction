// luxdrive/views/static/js/compare.js

let currentCarIds = [];

// Initialize
document.addEventListener('DOMContentLoaded', () => {
  // Read current ids from the template injection or URL
  const urlParams = new URLSearchParams(window.location.search);
  const idsStr = urlParams.get('ids');
  if (idsStr) {
    currentCarIds = idsStr.split(',').map(Number);
  }
});

// Tab Switching Logic
function switchTab(tabId) {
  // Update buttons
  document.querySelectorAll('.cmp-tab-btn').forEach(btn => {
    btn.classList.remove('active');
  });
  const activeBtn = document.querySelector(`.cmp-tab-btn[onclick="switchTab('${tabId}')"]`);
  if (activeBtn) activeBtn.classList.add('active');

  // Update sections
  document.querySelectorAll('.cmp-section').forEach(section => {
    section.classList.remove('active');
  });
  const activeSection = document.getElementById(`tab-${tabId}`);
  if (activeSection) activeSection.classList.add('active');
}

// Add Vehicle Modal
function openSearchModal() {
  if (currentCarIds.length >= 4) {
    alert('Bạn chỉ có thể so sánh tối đa 4 mẫu xe.');
    return;
  }
  const modal = document.getElementById('searchModal');
  if (modal) {
    modal.style.display = 'flex';
    document.getElementById('modalSearchInput').focus();
  }
}

function closeSearchModal() {
  const modal = document.getElementById('searchModal');
  if (modal) {
    modal.style.display = 'none';
  }
}

// Close modal on outside click
window.onclick = function(event) {
  const modal = document.getElementById('searchModal');
  if (event.target === modal) {
    closeSearchModal();
  }
}

// Loading state simulation
function simulateAILoading(callback) {
  const loader = document.getElementById('aiLoadingState');
  if (!loader) {
    callback();
    return;
  }
  
  loader.style.display = 'flex';
  const steps = loader.querySelectorAll('.loading-steps li');
  const bar = loader.querySelector('.progress-bar-fill');
  const text = loader.querySelector('.progress-text');
  
  let progress = 10;
  
  // Step 1
  setTimeout(() => {
    progress = 35;
    bar.style.width = progress + '%';
    text.innerText = 'Progress: ' + progress + '%';
    if(steps[0]) steps[0].className = 'done';
    if(steps[1]) steps[1].className = 'active';
  }, 400);

  // Step 2
  setTimeout(() => {
    progress = 68;
    bar.style.width = progress + '%';
    text.innerText = 'Progress: ' + progress + '%';
    if(steps[1]) steps[1].className = 'done';
    if(steps[2]) steps[2].className = 'active';
  }, 900);

  // Step 3
  setTimeout(() => {
    progress = 100;
    bar.style.width = progress + '%';
    text.innerText = 'Progress: ' + progress + '%';
    if(steps[2]) steps[2].className = 'done';
    if(steps[3]) steps[3].className = 'done';
  }, 1400);

  // Finish
  setTimeout(() => {
    loader.style.display = 'none';
    callback();
  }, 1600);
}

// Add car
function addCarToCompare(newId) {
  if (currentCarIds.includes(newId)) {
    closeSearchModal();
    return;
  }
  if (currentCarIds.length >= 4) {
    alert('Tối đa 4 mẫu xe.');
    return;
  }
  
  closeSearchModal();
  simulateAILoading(() => {
    const newIds = [...currentCarIds, newId];
    window.location.href = `/so-sanh?ids=${newIds.join(',')}`;
  });
}

// Remove car
function removeCar(removeId) {
  const newIds = currentCarIds.filter(id => id !== removeId);
  window.location.href = `/so-sanh?ids=${newIds.join(',')}`;
}

// Modal Search Filtering
function filterSearch() {
  const input = document.getElementById('modalSearchInput').value.toLowerCase();
  const items = document.querySelectorAll('.search-item');
  items.forEach(item => {
    const text = item.querySelector('.search-item-info h4').innerText.toLowerCase();
    if (text.includes(input)) {
      item.style.display = 'flex';
    } else {
      item.style.display = 'none';
    }
  });
}
