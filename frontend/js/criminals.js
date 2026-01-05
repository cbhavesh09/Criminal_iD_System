requireAuth();

const grid = document.getElementById("criminalGrid");
const form = document.getElementById("criminalForm");

/* ======================================================
   DETERMINISTIC ENCRYPTED THUMBNAIL (FOR EXISTING RECORDS)
====================================================== */
function generateStaticEncryptedThumbnail(seed) {
  const canvas = document.createElement("canvas");
  const ctx = canvas.getContext("2d");

  canvas.width = 300;
  canvas.height = 180;

  let hash = 0;
  for (let i = 0; i < seed.length; i++) {
    hash = seed.charCodeAt(i) + ((hash << 5) - hash);
  }

  for (let y = 0; y < canvas.height; y++) {
    for (let x = 0; x < canvas.width; x++) {
      const v = (hash + x * y) % 255;
      ctx.fillStyle = `rgb(${v}, ${(v * 7) % 255}, ${255 - v})`;
      ctx.fillRect(x, y, 1, 1);
    }
  }

  return canvas.toDataURL();
}

/* ======================================================
   LIVE ENCRYPTED PREVIEW (FOR NEW UPLOADS ONLY)
====================================================== */
function generateEncryptedPreview(file, callback) {
  const img = new Image();
  const reader = new FileReader();

  reader.onload = () => (img.src = reader.result);

  img.onload = () => {
    const canvas = document.createElement("canvas");
    const ctx = canvas.getContext("2d");

    canvas.width = 300;
    canvas.height = 180;

    ctx.drawImage(img, 0, 0, canvas.width, canvas.height);

    const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
    const data = imageData.data;

    for (let i = 0; i < data.length; i += 4) {
      const noise = Math.random() * 255;
      data[i] ^= noise;
      data[i + 1] ^= noise;
      data[i + 2] ^= noise;
    }

    ctx.putImageData(imageData, 0, 0);
    callback(canvas.toDataURL());
  };

  reader.readAsDataURL(file);
}

/* ======================================================
   LOAD CRIMINALS (DB RECORDS)
====================================================== */
async function loadCriminals() {
  const res = await fetch(`${API_BASE}/criminals`, {
    headers: authHeaders()
  });

  if (!res.ok) {
    alert("Failed to load criminal records");
    return;
  }

  const criminals = await res.json();
  grid.innerHTML = "";

  criminals.forEach(criminal => {
    const card = document.createElement("div");
    card.className = "criminal-card";

    const encryptedThumb = generateStaticEncryptedThumbnail(criminal._id);

    card.innerHTML = `
      <div class="image-container">
        <img
          src="${encryptedThumb}"
          data-id="${criminal._id}"
          onclick="decryptImage(this)"
          title="Click to decrypt"
        />
        <p class="encrypted-label">Encrypted Image</p>
      </div>

      <div class="info">
        <h4>${criminal.name}</h4>
        <p><strong>Case:</strong> ${criminal.caseNumber}</p>
        <p><strong>Status:</strong> ${criminal.status}</p>
      </div>
    `;

    grid.appendChild(card);
  });
}

/* ======================================================
   DECRYPT IMAGE ON CLICK
====================================================== */
async function decryptImage(imgElement) {
  const criminalId = imgElement.dataset.id;

  imgElement.style.opacity = "0.5";

  const res = await fetch(
    `${API_BASE}/criminals/${criminalId}/decrypt-image`,
    { headers: authHeaders() }
  );

  const data = await res.json();

  if (!res.ok) {
    alert(data.error || "Failed to decrypt image");
    imgElement.style.opacity = "1";
    return;
  }

  imgElement.src = `data:image/png;base64,${data.image}`;
  imgElement.style.opacity = "1";

  const label = imgElement.nextElementSibling;
  if (label) label.textContent = "Decrypted Image";
}

/* ======================================================
   ADD CRIMINAL (NO CASE NUMBER — AUTO GENERATED)
====================================================== */
form.addEventListener("submit", async (e) => {
  e.preventDefault();

 const name = form.querySelector('input[placeholder="Full Name"]').value.trim();
const ageValue = form.querySelector('input[type="number"]').value;
const charges = form.querySelector('input[placeholder^="Charges"]').value.trim();
const imageFile = form.querySelector('input[type="file"]').files[0];

const age = parseInt(ageValue, 10);

if (!name || !charges || !imageFile || isNaN(age) || age <= 0) {
  alert("Please enter a valid name, age, charges, and select an image");
  return;
}

  if (!name || !age || !charges || !imageFile) {
    alert("Please fill all fields and select an image");
    return;
  }

  // Show live encrypted preview immediately
  generateEncryptedPreview(imageFile, (previewSrc) => {
    const tempCard = document.createElement("div");
    tempCard.className = "criminal-card";

    tempCard.innerHTML = `
      <div class="image-container">
        <img src="${previewSrc}" />
        <p class="encrypted-label">Encrypted Image (Preview)</p>
      </div>
      <div class="info">
        <h4>${name}</h4>
        <p><strong>Status:</strong> pending</p>
      </div>
    `;

    grid.prepend(tempCard);
  });

  const formData = new FormData();
  formData.append("name", name);
  formData.append("age", age);
  formData.append("charges", charges);
  formData.append("image", imageFile);

  const res = await fetch(`${API_BASE}/criminals`, {
    method: "POST",
    headers: authHeaders(),
    body: formData
  });

  if (!res.ok) {
    const err = await res.json();
    alert(err.error || "Failed to add criminal");
    loadCriminals();
    return;
  }

  form.reset();
  loadCriminals();
});

/* ======================================================
   INITIAL LOAD
====================================================== */
loadCriminals();
