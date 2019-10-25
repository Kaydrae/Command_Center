<?php
/**
 * Created by PhpStorm.
 * User: KeOndrae
 * Date: 2019-09-20
 * Time: 16:33
 */

include_once "Credentials.php";

class Connection
{


    private $servername = "localhost";
    private $username = "root";
    private $database = "dashboard";
    private $password;
    private $conn;

    public function __construct(){

    }

    public function Connect()
    {
        $DatabasePass = new Credentials();
        $this->password = $DatabasePass->getDatabasePassword();

        try {
            $conn = new PDO("mysql:host=$this->servername;dbname=$this->database", $this->username, $this->password);
            // set the PDO error mode to exception
            $conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
            //echo "Connected successfully";

            return $conn;
        }
        catch(PDOException $e)
        {
            echo "Connection failed: " . $e->getMessage();
            die();
        }

    }

    public function Disconnect()
    {
        $this->conn = null;
    }

}