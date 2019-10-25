class TimeDate{

    constructor(date){

        this.hours   = date.getHours();
        this.minutes = date.getMinutes();
        this.seconds = date.getSeconds();
        this.utc     = date.getTime();
    }

    TimeNormal(){
        return moment(this.utc).format('hh:mm A');
    }

    TimeMilitary(){
        return moment(this.utc).format('kk:mm');
    }

    Date(){
        const DayofWeek = moment(this.utc).format('ddd');
        const month     = moment(this.utc).format('MMM');
        const day       = moment(this.utc).format('DD');

        return DayofWeek.toUpperCase() + ', ' + day + ' ' + month.toUpperCase();
    }



}