export async function askBackend(query) {
  const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/ask`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ query }),
  });

  if (!response.ok) {
    throw new Error("Failed to fetch from backend");
  }

  return response.json();
}
