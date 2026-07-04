<?php
// API endpoint (make sure this matches your local path)
$api = 'http://localhost/virtual_mouse_project_with_backend/backend/api/get_actions.php?limit=25';

// Fetch API response
$json = @file_get_contents($api);
$payload = $json ? json_decode($json, true) : ['ok' => false];
$data = $payload['data'] ?? [];
$latest = $data[0] ?? null;
?>
<!doctype html>
<html>
<head>
  <meta charset="utf-8" />
  <title>Virtual Mouse Dashboard</title>
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body class="bg-light">
<div class="container py-4">
  <h1 class="mb-4">Virtual Mouse Dashboard</h1>

  <div class="row g-3 mb-4">
    <div class="col-md-4">
      <div class="card shadow-sm">
        <div class="card-body">
          <h5 class="card-title">Latest</h5>
          <?php if ($latest): ?>
            <p class="card-text">
              <strong>Module:</strong> <?= htmlspecialchars($latest['module']) ?><br>
              <strong>Action:</strong> <?= htmlspecialchars($latest['action']) ?><br>
              <strong>Time:</strong> <?= htmlspecialchars($latest['created_at']) ?><br>
              <strong>From:</strong> <?= htmlspecialchars($latest['client_ip']) ?>
            </p>
          <?php else: ?>
            <p class="text-muted mb-0">No data yet.</p>
          <?php endif; ?>
        </div>
      </div>
    </div>
  </div>

  <div class="card shadow-sm">
    <div class="card-body">
      <h5 class="card-title">Recent Actions</h5>
      <div class="table-responsive">
        <table class="table table-sm">
          <thead>
            <tr>
              <th>ID</th>
              <th>Module</th>
              <th>Action</th>
              <th>IP</th>
              <th>Time</th>
              <th>Meta</th>
            </tr>
          </thead>
          <tbody>
          <?php if (!empty($data)): ?>
            <?php foreach ($data as $r): ?>
              <tr>
                <td><?= (int)$r['id'] ?></td>
                <td><?= htmlspecialchars($r['module']) ?></td>
                <td><?= htmlspecialchars($r['action']) ?></td>
                <td><?= htmlspecialchars($r['client_ip']) ?></td>
                <td><?= htmlspecialchars($r['created_at']) ?></td>
                <td><code><?= htmlspecialchars($r['meta'] ?? '') ?></code></td>
              </tr>
            <?php endforeach; ?>
          <?php else: ?>
            <tr><td colspan="6" class="text-muted text-center">No actions recorded yet.</td></tr>
          <?php endif; ?>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</div>
</body>
</html>
