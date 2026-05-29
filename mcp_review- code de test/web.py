const express = require('express');
const app = express();
const jwt = require('jsonwebtoken');

// --- P1 : SÉCURITÉ ---
// 1. Secret JWT en clair (Critique)
const JWT_SECRET = "super_secret_key_12345"; 

app.get('/admin', (req, res) => {
    const userRole = req.query.role;
    
    // 2. Logique de contrôle d'accès cassée
    if (userRole == "admin") {
        // 3. Injection de commande (RCE)
        const exec = require('child_process').exec;
        exec("echo Bienvenue " + req.query.name); 
        res.send("Accès autorisé");
    }
});

// --- P2 : CLEAN CODE ---
// Fonctions anonymes imbriquées et nommage pauvre
app.get('/data', function(req, res) {
    let a = [1, 2, 3];
    a.map(x => {
        console.log(x);
        return x * 2;
    });
    res.json({status: "ok"});
});

app.listen(3000);