const http = require("http");

const PORT = 5000;

const sendJson = (res, statusCode, body) => {
  res.writeHead(statusCode, {
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET,POST,PUT,PATCH,DELETE,OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type,Authorization",
  });
  res.end(JSON.stringify(body));
};

const server = http.createServer((req, res) => {
  if (req.method === "OPTIONS") {
    return sendJson(res, 200, { ok: true });
  }

  if (req.method === "GET" && req.url === "/health") {
    return sendJson(res, 200, { status: "ok" });
  }

  if (req.method === "POST" && req.url === "/auth/login") {
    return sendJson(res, 200, {
      token: "mock-token",
      user: { id: "dev-user" },
    });
  }

  return sendJson(res, 200, {
    ok: true,
    message: "Backend placeholder is running",
    method: req.method,
    path: req.url,
  });
});

server.listen(PORT, "0.0.0.0", () => {
  console.log(`Placeholder backend listening on port ${PORT}`);
});
