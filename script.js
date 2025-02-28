body {
    background-color: #1a1a1a;
    color: #fff;
    font-family: Arial, sans-serif;
    margin: 0;
    padding: 10px;
}

.container {
    max-width: 100%;
    margin: auto;
    text-align: center;
}

h1 {
    font-size: 24px;
    margin-bottom: 20px;
}

button {
    background-color: #007bff;
    color: white;
    border: none;
    padding: 10px 20px;
    font-size: 16px;
    cursor: pointer;
    border-radius: 5px;
}

button:hover {
    background-color: #0056b3;
}

table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 20px;
}

th, td {
    border: 1px solid #444;
    padding: 8px;
    font-size: 14px;
    text-align: left;
}

th {
    background-color: #333;
}

canvas {
    margin-top: 20px;
    width: 100% !important;
    max-height: 200px;
}

.modal {
    display: none;
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0,0,0,0.5);
}

.modal-content {
    background-color: #333;
    margin: 15% auto;
    padding: 20px;
    border: 1px solid #444;
    width: 80%;
    max-width: 500px;
    border-radius: 5px;
}

.close {
    color: #fff;
    float: right;
    font-size: 28px;
    font-weight: bold;
    cursor: pointer;
}

.close:hover {
    color: #007bff;
}

@media (max-width: 600px) {
    h1 { font-size: 20px; }
    button { font-size: 14px; padding: 8px 16px; }
    th, td { font-size: 12px; padding: 6px; }
    table { font-size: 12px; }
    .modal-content { width: 90%; margin: 20% auto; }
}
