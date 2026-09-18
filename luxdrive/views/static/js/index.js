// ===== DATA =====
const carData = {
  "Mercedes-Benz": {
    "C-Class": ["C200 Avantgarde", "C200 Avantgarde Plus", "C300 AMG"],
    "E-Class": ["E180", "E200 Exclusive", "E300 AMG"],
    "S-Class": ["S450", "S450 Luxury", "Maybach S480"],
    "GLC": ["GLC 200", "GLC 200 4MATIC", "GLC 300 4MATIC"]
  },
  "BMW": {
    "3 Series": ["320i Sport Line", "320i M Sport", "330i M Sport"],
    "5 Series": ["520i", "520i M Sport", "530i M Sport"],
    "X3": ["xDrive20i", "xDrive20i M Sport", "xDrive30i M Sport"],
    "X5": ["xDrive40i xLine", "xDrive40i M Sport", "xDrive40i xLine Plus"]
  },
  "Audi": {
    "A4": ["40 TFSI", "45 TFSI quattro"],
    "A6": ["45 TFSI", "55 TFSI quattro"],
    "Q5": ["45 TFSI quattro"],
    "Q7": ["45 TFSI quattro", "55 TFSI quattro"]
  },
  "Porsche": {
    "Macan": ["Macan", "Macan T", "Macan S", "Macan GTS"],
    "Cayenne": ["Cayenne", "Cayenne Platinum Edition", "Cayenne S", "Cayenne GTS"],
    "Panamera": ["Panamera", "Panamera 4", "Panamera 4S", "Panamera GTS"],
    "911": ["Carrera", "Carrera S", "Carrera 4S", "Turbo S", "GT3"]
  },
  "Lexus": {
    "ES": ["ES 250", "ES 250 F Sport", "ES 300h"],
    "RX": ["RX 350 Premium", "RX 350 Luxury", "RX 350 F Sport", "RX 500h F Sport Performance"],
    "NX": ["NX 350h", "NX 350 F Sport"],
    "LX": ["LX 600 Urban", "LX 600 VIP", "LX 600 F Sport"]
  },
  "Toyota": {
    "Camry": ["2.0G", "2.0Q", "2.5Q", "2.5HV"],
    "Fortuner": ["2.4 MT 4x2", "2.4 AT 4x2", "2.7 AT 4x2", "2.8 AT 4x4"],
    "Land Cruiser Prado": ["VX"],
    "Land Cruiser": ["LC300"]
  },
  "Honda": {
    "City": ["G", "L", "RS"],
    "Civic": ["E", "G", "RS", "Type R"],
    "CR-V": ["G", "L", "L AWD", "e:HEV RS"],
    "Accord": ["1.5 VTEC Turbo"]
  },
  "Ford": {
    "Ranger": ["XL", "XLS", "XLT", "Wildtrak", "Raptor"],
    "Everest": ["Ambiente", "Sport", "Titanium", "Titanium+"],
    "Explorer": ["Limited"],
    "Territory": ["Trend", "Titanium", "Titanium X"]
  },
  "Hyundai": {
    "Accent": ["1.4 MT", "1.4 AT", "1.4 AT Đặc biệt"],
    "Tucson": ["2.0 Tiêu chuẩn", "2.0 Đặc biệt", "1.6T Đặc biệt", "2.0D Đặc biệt"],
    "Santa Fe": ["2.5 Xăng Tiêu chuẩn", "2.2 Dầu Tiêu chuẩn", "2.5 Xăng Cao cấp", "2.2 Dầu Cao cấp"]
  },
  "Kia": {
    "K3": ["1.6 Deluxe", "1.6 Luxury", "1.6 Premium", "2.0 Premium", "1.6 Turbo"],
    "Seltos": ["1.4 Deluxe", "1.4 Luxury", "1.4 Premium", "1.6 Premium"],
    "Sorento": ["Luxury", "Premium", "Signature"],
    "Carnival": ["2.2D Luxury", "2.2D Premium", "2.2D Signature", "3.5G Signature"]
  },
  "Mazda": {
    "Mazda3": ["1.5L Deluxe", "1.5L Luxury", "1.5L Premium"],
    "Mazda6": ["2.0L Luxury", "2.0L Premium", "2.5L Signature Premium"],
    "CX-5": ["2.0L Deluxe", "2.0L Luxury", "2.0L Premium"],
    "CX-8": ["2.5L Luxury", "2.5L Premium", "2.5L Premium AWD"]
  },
  "VinFast": {
    "Fadil": ["Tiêu chuẩn", "Nâng cao", "Cao cấp"],
    "Lux A2.0": ["Tiêu chuẩn", "Nâng cao", "Cao cấp"],
    "Lux SA2.0": ["Tiêu chuẩn", "Nâng cao", "Cao cấp"],
    "VF 8": ["Eco", "Plus"],
    "VF 9": ["Eco", "Plus"]
  }
};

document.addEventListener('DOMContentLoaded', () => {
  const brandSelect = document.getElementById('brand');
  const modelSelect = document.getElementById('model');
  const variantSelect = document.getElementById('variant');
  const yearSelect = document.getElementById('year');

  if (brandSelect && modelSelect && variantSelect && yearSelect) {
    // Populate Brands
    Object.keys(carData).forEach(brand => {
      brandSelect.add(new Option(brand, brand));
    });

    // Populate Years
    const currentYear = new Date().getFullYear();
    for (let y = currentYear; y >= 2010; y--) {
      yearSelect.add(new Option(y, y));
    }

    // Handle Brand Change
    brandSelect.addEventListener('change', (e) => {
      modelSelect.innerHTML = '<option value="" disabled selected>Chọn dòng xe</option>';
      variantSelect.innerHTML = '<option value="" disabled selected>Chọn phiên bản</option>';

      const selectedBrand = e.target.value;
      const models = carData[selectedBrand];
      if (models) {
        Object.keys(models).forEach(model => {
          modelSelect.add(new Option(model, model));
        });
      }
      
      const badge = document.querySelector('.hero-badge');
      if (badge) {
        const popularBrands = ['Toyota', 'Honda', 'Mazda', 'Hyundai', 'Kia', 'Ford', 'VinFast'];
        if (popularBrands.includes(selectedBrand)) {
          badge.innerHTML = '<svg width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M12 2v4M12 18v4M4.93 4.93l2.83 2.83M16.24 16.24l2.83 2.83M2 12h4M18 12h4M4.93 19.07l2.83-2.83M16.24 7.76l2.83-2.83"/></svg> SMART MARKET VALUATION';
        } else {
          badge.innerHTML = '<svg width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M12 2v4M12 18v4M4.93 4.93l2.83 2.83M16.24 16.24l2.83 2.83M2 12h4M18 12h4M4.93 19.07l2.83-2.83M16.24 7.76l2.83-2.83"/></svg> AI POWERED VEHICLE VALUATION';
        }
      }
    });

    // Handle Model Change
    modelSelect.addEventListener('change', (e) => {
      variantSelect.innerHTML = '<option value="" disabled selected>Chọn phiên bản</option>';

      const brand = brandSelect.value;
      const model = e.target.value;
      const variants = carData[brand][model];

      if (variants) {
        variants.forEach(variant => {
          variantSelect.add(new Option(variant, variant));
        });
      }
    });
  }
});

// ===== NAVIGATION LOGIC =====
function scrollToValuation() {
  const formArea = document.getElementById('valuationForm');
  if (formArea) {
    formArea.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }
}

function formatMileageInput() {
  const input = document.getElementById('mileage');
  if (!input) return;
  const pos = input.selectionStart;
  const oldLen = input.value.length;
  let raw = input.value.replace(/[^0-9]/g, '');
  if (raw) {
    input.value = parseInt(raw, 10).toLocaleString('en-US');
  }
  const newLen = input.value.length;
  const newPos = Math.max(0, pos + (newLen - oldLen));
  input.setSelectionRange(newPos, newPos);
}

function validateODO() {
  const mileageInput = document.getElementById('mileage');
  const msgDiv = document.getElementById('odoValidationMsg');
  if (!mileageInput || !msgDiv) return;

  const mileage = parseInt(mileageInput.value.replace(/,/g, ''), 10);
  if (isNaN(mileage) || mileage <= 0) {
    msgDiv.className = 'inline-msg warning';
    msgDiv.textContent = '⚠ Vui lòng nhập ODO';
    msgDiv.style.color = '#EF4444';
  } else {
    msgDiv.className = 'inline-msg success';
    msgDiv.textContent = '✓ Hợp lệ';
    msgDiv.style.color = '#10B981';
  }
}

// ===== VALUATION API LOGIC =====
async function startValuation() {
  const btn = document.getElementById('btnSubmitVal');
  btn.innerHTML = '<span class="submit-icon">⏳</span> ĐANG PHÂN TÍCH...';
  btn.disabled = true;

  // Retrieve Form Data
  const brand = document.getElementById('brand').value || 'Mercedes-Benz';
  const model = document.getElementById('model').value || 'C-Class';
  const version = document.getElementById('version').value || 'Tiêu chuẩn';
  const year = document.getElementById('year').value || '2022';
  const mileage = document.getElementById('mileage').value.replace(/,/g, '') || '32500';
  const origin = document.getElementById('origin').value || 'Hà Nội';
  const owners = document.getElementById('owners').value || '1';

  // Map to backend payload
  const payload = {
    brand: brand,
    model: model,
    variant: version,
    year: year,
    mileage: mileage,
    accident_history: document.getElementById('no_accident').checked ? 0 : 1,
    flood_history: document.getElementById('no_accident').checked ? 0 : 1,
    owner_count: parseInt(owners),
    overall_condition: document.getElementById('good_tires').checked ? 'Tốt' : 'Trung bình'
  };

  try {
    const res = await fetch('/api/predict', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    const data = await res.json();

    // 1. HERO KẾT QUẢ
    document.getElementById('resTitle').innerText = `${brand} ${model} ${version}`;
    document.getElementById('resSubTags').innerHTML = `
      <span>Năm ${year}</span>
      <span>${parseInt(mileage).toLocaleString()} km</span>
      <span>Biển ${origin}</span>
    `;

    // 2. GIÁ TRỊ ĐỊNH GIÁ
    document.getElementById('resultPrice').innerText = data.price_formatted || (data.avg + ' đ');
    document.getElementById('resultRange').innerText = `${data.low} - ${data.high}`;
    
    // AI Confidence
    const conf = data.confidence || 94;
    document.getElementById('aiConfidenceText').innerText = conf + '%';
    document.getElementById('aiConfidenceBar').style.width = conf + '%';

    // 3. AI EXPLANATION (SHAP)
    const impactList = document.getElementById('shapImpactList');
    if (impactList && data.shap_insights) {
      impactList.innerHTML = '';
      data.shap_insights.forEach(insight => {
        const isPos = insight.impact === 'positive';
        impactList.innerHTML += `
          <div class="impact-item">
            <div class="impact-label">${insight.title} <span>${insight.description}</span></div>
            <div class="impact-progress">
              <div class="impact-bar" style="width: 70%; background: ${isPos ? '#10B981' : '#EF4444'}"></div>
            </div>
          </div>
        `;
      });
    }

    // 4. MARKET ANALYSIS
    if (document.getElementById('kpiAvg')) {
      document.getElementById('kpiAvg').innerText = data.avg;
      document.getElementById('kpiLow').innerText = data.low;
      document.getElementById('kpiHigh').innerText = data.high;
    }

    // Init Charts
    initCharts(data);

  } catch (e) {
    console.error('Valuation Error:', e);
  }

  // Restore button
  btn.innerHTML = '<span class="submit-icon">⚡</span> ĐỊNH GIÁ XE BẰNG AI';
  btn.disabled = false;
  
  // Scroll to result
  document.querySelector('.premium-dashboard').scrollIntoView({ behavior: 'smooth', block: 'start' });
}

// ===== CHARTS =====
function initCharts(data) {
  // Chart.js requires canvas contexts
  
  // 1. Market Distribution
  const ctxDist = document.getElementById('marketDistChart');
  if (ctxDist) {
    if (window.marketDistChart) window.marketDistChart.destroy();
    window.marketDistChart = new Chart(ctxDist, {
      type: 'bar',
      data: {
        labels: ['Rất thấp', 'Thấp', 'Trung bình', 'Cao', 'Rất cao'],
        datasets: [{
          label: 'Số lượng xe',
          data: [5, 12, 35, 18, 4],
          backgroundColor: '#4F46E5',
          borderRadius: 4
        }]
      },
      options: {
        responsive: true, maintainAspectRatio: false,
        plugins: { legend: { display: false } }
      }
    });
  }

  // 2. Price Forecast
  const ctxFore = document.getElementById('forecastChart');
  if (ctxFore) {
    if (window.forecastChart) window.forecastChart.destroy();
    window.forecastChart = new Chart(ctxFore, {
      type: 'line',
      data: {
        labels: ['Năm 1', 'Năm 2', 'Năm 3', 'Năm 4', 'Năm 5'],
        datasets: [{
          label: 'Giá trị dự kiến',
          data: [100, 92, 85, 79, 74], // Mock depreciation %
          borderColor: '#10B981',
          tension: 0.4, fill: true,
          backgroundColor: 'rgba(16, 185, 129, 0.1)'
        }]
      },
      options: {
        responsive: true, maintainAspectRatio: false,
        plugins: { legend: { display: false } },
        scales: { y: { display: false } }
      }
    });
  }

  // 3. Cost Donut
  const ctxCost = document.getElementById('costDonutChart');
  if (ctxCost) {
    if (window.costChart) window.costChart.destroy();
    window.costChart = new Chart(ctxCost, {
      type: 'doughnut',
      data: {
        labels: ['Nhiên liệu', 'Bảo dưỡng', 'Bảo hiểm', 'Khác'],
        datasets: [{
          data: [20, 15, 18, 8],
          backgroundColor: ['#4F46E5', '#10B981', '#F59E0B', '#94A3B8'],
          borderWidth: 0
        }]
      },
      options: {
        responsive: true, maintainAspectRatio: false,
        cutout: '75%',
        plugins: { legend: { display: false } }
      }
    });
  }
}
