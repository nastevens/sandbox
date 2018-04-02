subminder
=========

Subminder is a command line tool for creating subsequent task reminders with a
natural language interface. It runs on Linux (tested), Windows (tested), and I
see no reason it wouldn't run on OS X, although I haven't tried it.

Subsequent vs. Scheduled Tasks
==============================

Subminder is a tool for subsequent tasks, which are a little different than the
way that calendar tools like Google Calendar, Outlook, etc. think about tasks,
and a little bit different from a standard TODO list.  The easiest way to
explain is with an example.

Every dentist will tell you to floss your teeth every day. In a tool like
Outlook you could create a calendar reminder to floss your teeth and
set it up to repeat every day. While this might be okay for a few tasks it
quickly grows out of control. You could also set up a task that regenerates one
day after the previous task is completed. This works, but your completed tasks
end up sticking around long after you've done them.

In Subminder creating a reminder to floss your teeth every day is as easy as:
    
    add "Floss Teeth" daily

Each day when you run Subminder you'll see a list of tasks to do that day, and
each day Floss Teeth will appear on that list. When you mark the task complete
it will disappear - no completed task cluttering your list - and show up again
the next day.

More Complicated Example
========================

So that's an easy example - how about something more interesting. In the summer
I try to mow my lawn once a week so it doesn't grow into a jungle. I don't like
mowing during the week though, and since I live in Minnesota, I don't need to
mow the lawn in the winter. In Subminder I can create the task like this:

    add "Mow Lawn" on Saturday or Sunday May through October
    -or-
    add "Mow Lawn" Sat|Sun May-Oct

This will create a reminder that will show up each week in May through October
on Saturday at first. What if I don't mow the lawn until Sunday one week? In
that case, the following week the reminder will show up on Sunday as well - no
sense in mowing the lawn after only 6 days. What if I don't mow the lawn until
Wednesday? In this case Subminder will choose the matching weekday that doesn't
*exceed* the implied weekly spec, so the next reminder will occur on Sunday.

add "Mow Lawn" on Saturday or Sunday ([weekday or weekday] implies weekly)
add "Clean Cat Box" on Saturday and Sunday ([weekday and weekday] implies daily)
add "Labor Day" 1st Monday in Septembr ([first, last, second, third, etc] implies monthly)
add "Check Car Tires" 2nd last Saturday or last Saturday (implies monthly)
add "" first Saturday and last Saturday
