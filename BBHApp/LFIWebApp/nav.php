<?php
$items = json_decode(file_get_contents("nav.json"), true);
$navItems = [
  ["href" => "http://localhost:8081", "text" => "🏠 Home"],
  ["href" => "index.php?page=uploads/shell3.php", "text" => "💣 Trigger Shell"],
  ["href" => "index.php?page=uploads/shell_logs.txt", "text" => "📜 View Shell Logs"],
  ["href" => "http://localhost:8081", "text" => "🧪 SQLi Playground"],
  ["href" => "http://localhost:8082/reflected", "text" => "💉 Reflected XSS"],
  ["href" => "http://localhost:8082/stored", "text" => " 🗃 Stored XSS"],
  ["href" => "http://localhost:8082/dom", "text" => "🧠 DOM XSS"],
  ["href" => "http://localhost:8083", "text" => "🐚 LFI Playground"]
];
?>
<div style="margin-bottom: 20px;">
  <?php foreach ($navItems as $item): ?>
    <a href="<?= $item['href'] ?>" class="btn"><?= $item['text'] ?></a>
  <?php endforeach; ?>
</div>
<style>
  .btn {
    display: inline-block;
    background-color: #444;
    color: white;
    padding: 8px 12px;
    margin: 6px;
    text-decoration: none;
    border-radius: 6px;
  }
  .btn:hover {
    background-color: #666;
  }
</style>
