const API_URL = process.env.NEXT_PUBLIC_PASTELY_API_URL;

async function retrievePaste(id) {
  const data = await fetch(`${API_URL}/${id}`);
  return data.json();
}

async function submitPaste(data) {
  return await fetch(`${API_URL}/`, {
    method: "post",
    body: JSON.stringify(data),
  });
}

export default { retrievePaste, submitPaste };
