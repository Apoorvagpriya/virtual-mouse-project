<?php
require_once __DIR__ . '/config.php';

$body = json_decode(file_get_contents('php://input'), true);
$module = $body['module'] ?? $_POST['module'] ?? null;
$action = $body['action'] ?? $_POST['action'] ?? 'select';
$meta   = $body['meta']   ?? $_POST['meta']   ?? null;
$ip     = $_SERVER['REMOTE_ADDR'] ?? null;

$validModules = ['eye','hand','voice'];
$validActions = ['select','start','stop'];

if (!in_array($module, $validModules, true)) {
  http_response_code(400);
  echo json_encode(['ok'=>false,'error'=>'Invalid module']);
  exit;
}
if (!in_array($action, $validActions, true)) {
  http_response_code(400);
  echo json_encode(['ok'=>false,'error'=>'Invalid action']);
  exit;
}

$stmt = $mysqli->prepare("INSERT INTO actions (module, action, client_ip, meta) VALUES (?,?,?,?)");
$metaStr = is_array($meta) ? json_encode($meta, JSON_UNESCAPED_UNICODE) : (is_string($meta) ? $meta : null);
$stmt->bind_param('ssss', $module, $action, $ip, $metaStr);

if (!$stmt->execute()) {
  http_response_code(500);
  echo json_encode(['ok'=>false,'error'=>'Insert failed','detail'=>$stmt->error]);
  exit;
}

echo json_encode(['ok'=>true,'id'=>$stmt->insert_id]);
?>
