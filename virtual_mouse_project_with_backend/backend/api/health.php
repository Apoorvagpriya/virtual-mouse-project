<?php
require_once __DIR__ . '/config.php';
echo json_encode(['ok' => true, 'service' => 'virtual-mouse-api', 'time' => date('c')]);
?>
