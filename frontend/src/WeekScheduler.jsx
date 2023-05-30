import React, {useEffect, useState} from 'react';
import Paper from '@mui/material/Paper';
import {
  Scheduler,
  WeekView,
  Appointments,
} from '@devexpress/dx-react-scheduler-material-ui';
import axios from 'axios';

function WeekScheduler() {
  const [tasks, setTasks] = useState([]);
  const currentDate = new Date();
  const currentWeekday = currentDate.getDay(); // Sunday: 0, Monday: 1, ..., Saturday: 6

  // Convert weekday to 1-7 mapping
  let convertedWeekday = currentWeekday === 0 ? 7 : currentWeekday;


  useEffect(() => {
    axios.get('/api/tasks').then( (response) => {
      console.log(response)
      return setTasks(parseData(response.data))})
  }, [])
  


  const parseData = data => {
    let result = [];

    const weekdays = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"];

    let count = 0

    for (let i = 0; i < weekdays.length; i++) {
      const day = weekdays[i];
      const events = data[day];
      const eventKeys = Object.entries(events);
      Object.entries(eventKeys).forEach(([key, value]) => {
        const eventTitle = value[0];
        const eventTimes = value[1];
        const startDate = new Date();
        startDate.setDate(startDate.getDate() + (7 + (i - startDate.getDay() + 1)) % 7);
        startDate.setHours(eventTimes[0], 0, 0, 0);

        const endDate = new Date(startDate);
        endDate.setHours(eventTimes[1], 0, 0, 0);

        result.push({
          title: eventTitle,
          startDate,
          endDate,
          id: count,
        });
        ++count;
     });
    }
    return result;
  };



  return (
    <Paper>
      <Scheduler data={tasks} height={"auto"} firstDayOfWeek={convertedWeekday}>
        <WeekView startDayHour={8.5} endDayHour={21.1} />
        <Appointments />
      </Scheduler>
    </Paper>
  )
}




export default WeekScheduler;