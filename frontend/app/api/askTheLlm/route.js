export async function POST(request) {
  try {
    // Get request body (JSON)
    const body = await request.json();
    
    // Get backend URL from environment (server-side only)
    // This env var is NOT available to the browser
    const backendUrl = process.env.INTERNAL_API_URL || 
                       process.env.NEXT_PUBLIC_ASK_LEAFY_API_URL || 
                       "http://localhost:8000";
    
    // Build full backend URL
    const url = `${backendUrl}/askTheLlm`;
    
    console.log(`🔗 Proxying POST request to: ${url}`);
    
    // Forward request to backend
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(body),
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: 'Request failed' }));
      return Response.json(error, { status: response.status });
    }

    const data = await response.json();
    return Response.json(data);
  } catch (error) {
    console.error('❌ Proxy error:', error);
    return Response.json(
      { error: 'Failed to connect to backend', details: error.message },
      { status: 500 }
    );
  }
}