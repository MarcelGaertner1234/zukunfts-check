<?php
// Fehlerberichterstattung für Debugging (in Produktion auskommentieren)
// error_reporting(E_ALL);
// ini_set('display_errors', 1);

// CORS Headers für AJAX-Requests
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: POST');
header('Access-Control-Allow-Headers: Content-Type');
header('Content-Type: application/json; charset=utf-8');

// Nur POST-Requests erlauben
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(['success' => false, 'message' => 'Nur POST-Requests erlaubt']);
    exit;
}

// Empfänger E-Mail
$to = 'gaertner-marcel@web.de';

// Formulardaten empfangen und validieren
$name = isset($_POST['name']) ? trim($_POST['name']) : '';
$email = isset($_POST['email']) ? trim($_POST['email']) : '';
$phone = isset($_POST['phone']) ? trim($_POST['phone']) : '';
$message = isset($_POST['message']) ? trim($_POST['message']) : '';

// Validierung
$errors = [];

if (empty($name)) {
    $errors[] = 'Name ist erforderlich';
}

if (empty($email)) {
    $errors[] = 'E-Mail ist erforderlich';
} elseif (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
    $errors[] = 'Ungültige E-Mail-Adresse';
}

if (empty($message)) {
    $errors[] = 'Nachricht ist erforderlich';
}

// Wenn Fehler vorhanden sind, zurückgeben
if (!empty($errors)) {
    http_response_code(400);
    echo json_encode([
        'success' => false,
        'message' => 'Bitte korrigieren Sie die folgenden Fehler:',
        'errors' => $errors
    ]);
    exit;
}

// E-Mail vorbereiten
$subject = 'Neue Kontaktanfrage von FutureCheck Website';

// HTML E-Mail Body
$htmlBody = "
<!DOCTYPE html>
<html>
<head>
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
        .container { max-width: 600px; margin: 0 auto; padding: 20px; }
        .header { background: linear-gradient(135deg, #667EEA 0%, #764BA2 100%); color: white; padding: 30px; border-radius: 10px 10px 0 0; }
        .content { background: #f8f9fa; padding: 30px; border-radius: 0 0 10px 10px; }
        .field { margin-bottom: 20px; }
        .label { font-weight: bold; color: #667EEA; margin-bottom: 5px; }
        .value { background: white; padding: 10px; border-radius: 5px; border-left: 3px solid #667EEA; }
        .message-box { background: white; padding: 15px; border-radius: 5px; border-left: 3px solid #667EEA; white-space: pre-wrap; }
        .footer { margin-top: 30px; padding-top: 20px; border-top: 1px solid #ddd; text-align: center; color: #666; font-size: 12px; }
    </style>
</head>
<body>
    <div class='container'>
        <div class='header'>
            <h2 style='margin: 0;'>Neue Kontaktanfrage</h2>
            <p style='margin: 10px 0 0 0; opacity: 0.9;'>Über das FutureCheck Kontaktformular</p>
        </div>
        <div class='content'>
            <div class='field'>
                <div class='label'>Name:</div>
                <div class='value'>" . htmlspecialchars($name) . "</div>
            </div>
            
            <div class='field'>
                <div class='label'>E-Mail:</div>
                <div class='value'><a href='mailto:" . htmlspecialchars($email) . "'>" . htmlspecialchars($email) . "</a></div>
            </div>
            
            " . (!empty($phone) ? "
            <div class='field'>
                <div class='label'>Telefon:</div>
                <div class='value'><a href='tel:" . htmlspecialchars($phone) . "'>" . htmlspecialchars($phone) . "</a></div>
            </div>
            " : "") . "
            
            <div class='field'>
                <div class='label'>Nachricht:</div>
                <div class='message-box'>" . nl2br(htmlspecialchars($message)) . "</div>
            </div>
            
            <div class='footer'>
                <p>Diese Nachricht wurde am " . date('d.m.Y \u\m H:i \U\h\r') . " gesendet.</p>
                <p>IP-Adresse: " . $_SERVER['REMOTE_ADDR'] . "</p>
            </div>
        </div>
    </div>
</body>
</html>
";

// Plain Text Alternative
$textBody = "Neue Kontaktanfrage von FutureCheck Website\n";
$textBody .= "==========================================\n\n";
$textBody .= "Name: " . $name . "\n";
$textBody .= "E-Mail: " . $email . "\n";
if (!empty($phone)) {
    $textBody .= "Telefon: " . $phone . "\n";
}
$textBody .= "\nNachricht:\n" . $message . "\n\n";
$textBody .= "--------------------\n";
$textBody .= "Gesendet am: " . date('d.m.Y H:i') . "\n";
$textBody .= "IP-Adresse: " . $_SERVER['REMOTE_ADDR'] . "\n";

// E-Mail Headers
$headers = [
    'MIME-Version: 1.0',
    'Content-Type: text/html; charset=UTF-8',
    'From: FutureCheck Website <noreply@' . $_SERVER['HTTP_HOST'] . '>',
    'Reply-To: ' . $name . ' <' . $email . '>',
    'X-Mailer: PHP/' . phpversion()
];

// E-Mail senden
$mailSent = mail($to, $subject, $htmlBody, implode("\r\n", $headers));

// Bestätigungs-E-Mail an den Absender
if ($mailSent) {
    $confirmSubject = 'Ihre Anfrage bei FutureCheck';
    $confirmBody = "
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
            .container { max-width: 600px; margin: 0 auto; padding: 20px; }
            .header { background: linear-gradient(135deg, #3B82F6 0%, #60A5FA 100%); color: white; padding: 30px; border-radius: 10px 10px 0 0; text-align: center; }
            .content { background: #f8f9fa; padding: 30px; border-radius: 0 0 10px 10px; }
            .button { display: inline-block; padding: 12px 30px; background: #3B82F6; color: white; text-decoration: none; border-radius: 5px; margin-top: 20px; }
        </style>
    </head>
    <body>
        <div class='container'>
            <div class='header'>
                <h2 style='margin: 0;'>Vielen Dank für Ihre Anfrage!</h2>
            </div>
            <div class='content'>
                <p>Hallo " . htmlspecialchars($name) . ",</p>
                <p>wir haben Ihre Nachricht erhalten und werden uns schnellstmöglich bei Ihnen melden.</p>
                <p><strong>Ihre Anfrage:</strong></p>
                <div style='background: white; padding: 15px; border-radius: 5px; margin: 20px 0;'>
                    " . nl2br(htmlspecialchars($message)) . "
                </div>
                <p>Bei dringenden Anliegen erreichen Sie uns auch telefonisch unter: <strong>+41 76 801 53 30</strong></p>
                <p>Mit freundlichen Grüßen<br>Ihr FutureCheck Team</p>
            </div>
        </div>
    </body>
    </html>
    ";
    
    $confirmHeaders = [
        'MIME-Version: 1.0',
        'Content-Type: text/html; charset=UTF-8',
        'From: FutureCheck <noreply@' . $_SERVER['HTTP_HOST'] . '>',
        'X-Mailer: PHP/' . phpversion()
    ];
    
    mail($email, $confirmSubject, $confirmBody, implode("\r\n", $confirmHeaders));
}

// Response
if ($mailSent) {
    echo json_encode([
        'success' => true,
        'message' => 'Vielen Dank für Ihre Nachricht! Wir werden uns schnellstmöglich bei Ihnen melden.'
    ]);
} else {
    http_response_code(500);
    echo json_encode([
        'success' => false,
        'message' => 'Beim Senden Ihrer Nachricht ist ein Fehler aufgetreten. Bitte versuchen Sie es später erneut oder kontaktieren Sie uns direkt per E-Mail.'
    ]);
}
?>