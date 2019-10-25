<?php
/**
 * Created by PhpStorm.
 * User: KeOndrae
 * Date: 2019-09-20
 * Time: 16:45
 *
 * Php handler for Rooms class
 */

require_once "../php/Room.php";

$Calling = $_GET['Calling'];

switch ($Calling){

    case 'GetAllRooms':
        GetAllRooms();
        break;
}

function GetAllRooms(){

    $AllRooms = new Room();
    $results = $AllRooms->GetAllRooms();
    echo json_encode($results);

}