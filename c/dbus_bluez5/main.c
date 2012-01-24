#include <dbus/dbus.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

struct adapter
{
    char address[18];
    char name[128];
    char alias[128];
    uint32_t class;
    dbus_bool_t powered;
    dbus_bool_t discoverable;
    uint32_t discoverable_timeout;
    dbus_bool_t pairable;
    uint32_t pairable_timeout;
    dbus_bool_t discovering;
};

static void
exit_with_error ( char * const message )
{
    printf("%s\n", message);
    exit(1);
}

static void
exit_with_dbus_error (
        char * const message,
        DBusError * const error )
{
    printf("%s: %s\n", message, error->message);
    if (NULL != error)
    {
        dbus_error_free(error);
    }
    exit(1);
}

static DBusConnection *
open_system_bus ( void )
{
    DBusError error;
    DBusConnection * connection = NULL;

    dbus_error_init(&error);

    connection = dbus_bus_get(DBUS_BUS_SYSTEM, &error);

    if (dbus_error_is_set(&error))
    {
        exit_with_dbus_error("Could not get system bus", &error);
    }

    return connection;
}

/* static void */
/* close_system_bus ( DBusConnection * const connection ) */
/* { */
/*     if (NULL != connection) */
/*     { */
/*         dbus_connection_close(connection); */
/*     } */
/* } */

static dbus_bool_t
open_dict_read (
        DBusMessageIter * const iter,
        DBusMessageIter * const iter_dict )
{
    if (NULL == iter || NULL == iter_dict)
    {
        return FALSE;
    }

    if (dbus_message_iter_get_arg_type(iter) != DBUS_TYPE_ARRAY)
    {
        return FALSE;
    }

    if (dbus_message_iter_get_element_type(iter) != DBUS_TYPE_DICT_ENTRY)
    {
        return FALSE;
    }

    dbus_message_iter_recurse(iter, iter_dict);
    return TRUE;
}

static dbus_bool_t
read_next_object_path_entry (
        DBusMessageIter * const iter_object_paths,
        char ** const object_path,
        DBusMessageIter * const iter_interfaces )
{
    DBusMessageIter iter_dict_entry;

    if (!iter_object_paths || !iter_interfaces)
    {
        goto error;
    }

    if (dbus_message_iter_get_arg_type(iter_object_paths) != DBUS_TYPE_DICT_ENTRY)
    {
        goto error;
    }

    dbus_message_iter_recurse(iter_object_paths, &iter_dict_entry);

    if (dbus_message_iter_get_arg_type(&iter_dict_entry) != DBUS_TYPE_OBJECT_PATH)
    {
        exit_with_error("Unexpected arg type for object path");
    }

    dbus_message_iter_get_basic(&iter_dict_entry, object_path);

    dbus_message_iter_next(&iter_dict_entry);

    if (FALSE == open_dict_read(&iter_dict_entry, iter_interfaces))
    {
        goto error;
    }

    dbus_message_iter_next(iter_object_paths);

    return TRUE;

error:
    return FALSE;
}

static dbus_bool_t
read_next_interface_entry (
        DBusMessageIter * const interface_dict,
        char ** const interface )
{
    DBusMessageIter iter_dict_entry;

    if (!interface_dict)
    {
        goto error;
    }

    if (dbus_message_iter_get_arg_type(interface_dict) != DBUS_TYPE_DICT_ENTRY)
    {
        goto error;
    }

    dbus_message_iter_recurse(interface_dict, &iter_dict_entry);

    if (dbus_message_iter_get_arg_type(&iter_dict_entry) != DBUS_TYPE_STRING)
    {
        exit_with_error("Unexpected arg type for interface");
    }

    dbus_message_iter_get_basic(&iter_dict_entry, interface);

    dbus_message_iter_next(interface_dict);

    return TRUE;

error:
    return FALSE;
}


static void
list_adapters ( DBusConnection * const connection )
{
    DBusError error;
    DBusMessage * msg = NULL;
    DBusMessage * rsp = NULL;
    DBusMessageIter args;
    DBusMessageIter subargs;
    DBusMessageIter interface_iter;
    char * object_path = NULL;
    char * interface = NULL;
    char const * const adapter = "org.bluez.Adapter1";

    dbus_error_init(&error);

    msg = dbus_message_new_method_call("org.bluez",
                                       "/",
                                       "org.freedesktop.DBus.ObjectManager",
                                       "GetManagedObjects");
    if (NULL == msg)
    {
        exit_with_error("Could not obtain method call");
    }

    /* No arguments */

    /* Invoke the method */
    rsp = dbus_connection_send_with_reply_and_block(connection,
                                                    msg,
                                                    DBUS_TIMEOUT_USE_DEFAULT,
                                                    &error);
    if (dbus_error_is_set(&error))
    {
        exit_with_dbus_error("Could not GetManagedObjects", &error);
    }

    if (NULL == rsp)
    {
        exit_with_error("Response was NULL");
    }

    if (!dbus_message_iter_init(rsp, &args))
    {
        exit_with_error("Could not start message iterator on response");
    }

    if (!open_dict_read(&args, &subargs))
    {
        exit_with_error("Could not start dict read");
    }

    /* Print out the object paths */
    printf("Printing object paths\n");

    while (FALSE != read_next_object_path_entry(&subargs, &object_path, &interface_iter))
    {
        /* dbus_bool_t found = FALSE; */
        printf("Object path: %s\n", object_path);
        while (FALSE != read_next_interface_entry(&interface_iter, &interface))
        {
            printf("  Interface: %s\n", interface);
        }
    }
    printf("Printed all object paths\n");

    if (NULL != rsp)
    {
        dbus_message_unref(rsp);
    }

    if (NULL != msg)
    {
        dbus_message_unref(msg);
    }
}

static void
get_adapter_string_property (
        DBusConnection * const connection,
        char const * const adapter,
        char const * const name,
        char * const property_value,
        uint32_t value_len_max )
{
    DBusError error;
    DBusMessage * msg = NULL;
    DBusMessage * rsp = NULL;
    DBusMessageIter args;
    DBusMessageIter subargs;
    dbus_bool_t status = FALSE;
    char * tmp_pchar = NULL;

    dbus_error_init(&error);

    printf("Creating method call\n");
    msg = dbus_message_new_method_call("org.bluez",
                                       adapter,
                                       "org.freedesktop.DBus.Properties",
                                       "Get");
    if (NULL == msg)
    {
        exit_with_error("Could not obtain method call");
    }

    /* Initialize arguments */
    printf("Initializing arguments\n");
    char const * adapter_interface = "org.bluez.Adapter1";
    status = dbus_message_append_args(msg,
                                      DBUS_TYPE_STRING, &adapter_interface,
                                      DBUS_TYPE_STRING, &name,
                                      DBUS_TYPE_INVALID);
    if (FALSE == status)
    {
        exit_with_error("Cannot append arguments to Properties.Get");
    }

    /* Invoke the method */
    printf("Invoking method\n");
    rsp = dbus_connection_send_with_reply_and_block(connection,
                                                    msg,
                                                    DBUS_TIMEOUT_USE_DEFAULT,
                                                    &error);
    if (dbus_error_is_set(&error))
    {
        exit_with_dbus_error("Could not invoke Properties.Get", &error);
    }

    if (NULL == rsp)
    {
        exit_with_error("Response was NULL");
    }

    printf("Starting iteration\n");
    if (!dbus_message_iter_init(rsp, &args))
    {
        exit_with_error("Could not start message iterator on response");
    }

    if (DBUS_TYPE_VARIANT != dbus_message_iter_get_arg_type(&args))
    {
        exit_with_error("Property return value is not a variant");
    }

    dbus_message_iter_recurse(&args, &subargs);

    if (DBUS_TYPE_STRING != dbus_message_iter_get_arg_type(&subargs))
    {
        exit_with_error("Contents of property variant was not a string");
    }

    dbus_message_iter_get_basic(&subargs, &tmp_pchar);

    printf("Copying returned string\n");
    strncpy(property_value, tmp_pchar, value_len_max);
    property_value[value_len_max - 1] = '\0';

    if (NULL != rsp)
    {
        dbus_message_unref(rsp);
    }

    if (NULL != msg)
    {
        dbus_message_unref(msg);
    }

}

int main(int argc, char *argv[])
{
    DBusConnection *connection = NULL;
    char buffer[128] = { 0 };

    connection = open_system_bus();
    if (NULL == connection)
    {
        exit_with_error("open_system_bus returned NULL");
    }

    list_adapters(connection);

    get_adapter_string_property(connection,
                                "/org/bluez/hci0",
                                "Address",
                                buffer,
                                sizeof buffer);
    printf("Address hci0: %s\n", buffer);

    // Do not close system bus - causes DBus error
//    close_system_bus(connection);

    return 0;
}
