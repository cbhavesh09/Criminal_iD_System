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
   LOAD CRIMINALS
====================================================== */
async function loadCriminals() {
  const res = await fetch(`${API_BASE}/api/criminals`, {
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
          ondblclick="decryptImage(this)"
          title="Double-click to decrypt"
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
   DECRYPT IMAGE
====================================================== */
async function decryptImage(img) {
  const id = img.dataset.id;

  const res = await fetch(
    `${API_BASE}/api/criminals/${id}/decrypt-image`,
    { headers: authHeaders() }
  );

  const data = await res.json();

  if (!res.ok) {
    alert(data.error || "Failed to decrypt image");
    return;
  }

  img.src = `data:image/png;base64,${data.image}`;
  img.nextElementSibling.textContent = "Decrypted Image";
}

/* ======================================================
   ADD CRIMINAL
====================================================== */
form.addEventListener("submit", async (e) => {
  e.preventDefault();

  const name = form.querySelector('input[placeholder="Full Name"]').value.trim();
  const age = parseInt(form.querySelector('input[type="number"]').value, 10);
  const charges = form.querySelector('input[placeholder^="Charges"]').value.trim();
  const imageFile = form.querySelector('input[type="file"]').files[0];

  if (!name || !charges || !imageFile || isNaN(age) || age <= 0) {
    alert("Please fill all fields correctly");
    return;
  }

  const formData = new FormData();
  formData.append("name", name);
  formData.append("age", age);
  formData.append("charges", charges);
  formData.append("image", imageFile);

  const res = await fetch(`${API_BASE}/api/criminals`, {
    method: "POST",
    headers: authHeaders(),
    body: formData
  });

  if (!res.ok) {
    const err = await res.json();
    alert(err.error || "Failed to add criminal");
    return;
  }

  form.reset();
  loadCriminals();
});

/* ======================================================
   INIT
====================================================== */
loadCriminals();
