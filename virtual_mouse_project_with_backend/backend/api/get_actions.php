<?php
require_once __DIR__ . '/config.php';

$limit = isset($_GET['limit']) ? max(1, min((int)$_GET['limit'], 200)) : 50;
$latestOnly = isset($_GET['latest']);

if ($latestOnly) {
  $sql = "SELECT id, module, action, client_ip, meta, created_at
          FROM actions ORDER BY id DESC LIMIT 1";
} else {
  $sql = "SELECT id, module, action, client_ip, meta, created_at
          FROM actions ORDER BY id DESC LIMIT ".$limit;
}

$res = $mysqli->query($sql);
$data = [];
while ($row = $res->fetch_assoc()) { $data[] = $row; }

echo json_encode(['ok'=>true, 'count'=>count($data), 'data'=>$data]);
?>
