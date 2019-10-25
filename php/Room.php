<?php
/**
 * Created by PhpStorm.
 * User: KeOndrae
 * Date: 2019-09-17
 * Time: 19:20
 */

include_once "../Connection/Connection.php";

class Room
{
    //Private Variables


    public function __construct()
    {

    }

    public function __destruct()
    {

    }

    public function CreateRoom()
    {

    }

    public function EditRoom()
    {

    }

    public function GetAllRooms()
    {

        $conn = new Connection();

        if($conn->Connect()){
            $dataArray[] = array();
            $query = "SELECT * FROM Room WHERE Enable = ?";
            $result = $conn->Connect()->prepare($query);
            $result-> execute([1]);
            $data = $result-> fetchall();

             foreach ($data as $row) {
                 $dataArray[] = array(
                     'ID'         => $row['ID'],
                     'Name'       => $row['Name'],
                     'ImageSmall' => $row['ImageSmall'],
                     'ImageBig'   => $row['ImageBig'],
                     'Desc'       => $row['Desc']

                 );

            }

            $conn->Disconnect();
            return $dataArray;


        }else{
            echo json_encode('error');
        }





    }

    public function DisplayRoom(){

    }

}