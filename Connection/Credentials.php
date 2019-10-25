<?php
/**
 * Created by PhpStorm.
 * User: Ke'Ondrae
 * Date: 2019-09-20
 * Time: 14:43
 * Class is for the Credentials of the database and other things that
 * will be password protected.
 * AKA Master password list
 */


class Credentials
{
    //Database
    private $databasePassword = "root";

    public function __construct(){


    }

    public function setDatabasePassword($databasePassword){
        $this->databasePassword = $databasePassword;
    }


    public function getDatabasePassword(){

        return $this->databasePassword;
    }



}