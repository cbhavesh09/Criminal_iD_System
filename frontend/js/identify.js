requireAuth();

const form = document.getElementById("identifyForm");
const loader = document.getElementById("loader");
const resultSection = document.getElementById("result");

const uploadedImgEl = document.getElementById("uploadedImage");
const dbImgEl = document.getElementById("dbImage");
const detailsEl = document.getElementById("details");

form.addEventListener("submit", async (e) => {
  e.preventDefault();

  const file = form.elements[0].files[0];
  if (!file) return;

  resultSection.classList.add("hidden");
  loader.classList.remove("hidden");

  uploadedImgEl.src = URL.createObjectURL(file);

  const formData = new FormData();
  formData.append("image", file);

  const res = await fetch(`${API_BASE}/api/identify`, {
    method: "POST",
    headers: authHeaders(),
    body: formData
  });

  const data = await res.json();
  loader.classList.add("hidden");

  if (!res.ok) {
    alert(data.error || "Identification failed");
    return;
  }

  if (!data.match) {
    alert("No matching criminal found");
    return;
  }

  const criminal = data.criminal;

  const imgRes = await fetch(
    `${API_BASE}/api/criminals/${criminal._id}/decrypt-image`,
    { headers: authHeaders() }
  );

  const imgData = await imgRes.json();

  if (!imgRes.ok) {
    alert("Failed to fetch database image");
    return;
  }

  dbImgEl.src = `data:image/png;base64,${imgData.image}`;

  detailsEl.innerHTML = `
    <p><strong>Name:</strong> ${criminal.name}</p>
    <p><strong>Case Number:</strong> ${criminal.caseNumber}</p>
    <p><strong>Age:</strong> ${criminal.age}</p>
    <p><strong>Charges:</strong> ${criminal.charges.join(", ")}</p>
    <p><strong>Status:</strong> ${criminal.status}</p>
  `;

  resultSection.classList.remove("hidden");
});
