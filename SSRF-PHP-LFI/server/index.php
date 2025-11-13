<!DOCTYPE html>
<html>
  <head>
    <title>LFI worldend</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+Mono&display=swap" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+Mono:wght@700&display=swap" rel="stylesheet">
    <style>
      body {
        font-family: 'Noto Sans Mono', monospace;
      }
    </style>
  </head>
    <h1>LFI worldend</h1>
    <?php
      if (isset($_GET['page'])) {
        include($_GET['page']);
      }      
    ?>
    <a href='?page=./page/pear.php'>Pear</a>
    <a href='?page=./page/apple.php'>Apple</a>
    <hr>
    <div style="display: inline-block;background-color: rgba(0,0,0,0.1);"><?php highlight_file(__FILE__); ?></div>
</html>