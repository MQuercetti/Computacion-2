import argparse
import json
import sys
from pathlib import Path

DATA_FILE = Path(__file__).with_name("tareas_db.json")
PRIORITIES = ["baja", "media", "alta"]


def load_tasks():
    if not DATA_FILE.exists():
        return []

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
    except json.JSONDecodeError as error:
        print(f"Error: base de tareas invalida: {error}", file=sys.stderr)
        sys.exit(1)
    except OSError as error:
        print(f"Error: no se pudo leer la base de tareas: {error}", file=sys.stderr)
        sys.exit(1)

    if not isinstance(data, list):
        print("Error: base de tareas invalida (se esperaba una lista)", file=sys.stderr)
        sys.exit(1)

    return data


def save_tasks(tasks):
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as file:
            json.dump(tasks, file, ensure_ascii=False, indent=2)
            file.write("\n")
    except OSError as error:
        print(f"Error: no se pudo guardar la base de tareas: {error}", file=sys.stderr)
        sys.exit(1)


def next_id(tasks):
    if not tasks:
        return 1
    return max(task["id"] for task in tasks) + 1


def find_task(tasks, task_id):
    for task in tasks:
        if task["id"] == task_id:
            return task
    return None


def build_parser():
    parser = argparse.ArgumentParser(description="Administrador simple de tareas")
    subparsers = parser.add_subparsers(dest="command", required=True)

    add_parser = subparsers.add_parser("add", help="Agrega una nueva tarea")
    add_parser.add_argument(
        "descripcion",
        nargs="+",
        help="Descripcion de la tarea",
    )
    add_parser.add_argument(
        "--priority",
        choices=PRIORITIES,
        default="media",
        help="Prioridad de la tarea (default: media)",
    )

    list_parser = subparsers.add_parser("list", help="Lista tareas")
    status_group = list_parser.add_mutually_exclusive_group()
    status_group.add_argument(
        "--pending",
        action="store_true",
        help="Muestra solo tareas pendientes",
    )
    status_group.add_argument(
        "--done",
        action="store_true",
        help="Muestra solo tareas completadas",
    )
    list_parser.add_argument(
        "--priority",
        choices=PRIORITIES,
        help="Filtra por prioridad",
    )

    done_parser = subparsers.add_parser("done", help="Marca tarea como completada")
    done_parser.add_argument("id", type=int, help="ID de la tarea")

    remove_parser = subparsers.add_parser("remove", help="Elimina una tarea")
    remove_parser.add_argument("id", type=int, help="ID de la tarea")

    return parser


def command_add(args):
    tasks = load_tasks()
    description = " ".join(args.descripcion)

    task = {
        "id": next_id(tasks),
        "descripcion": description,
        "priority": args.priority,
        "done": False,
    }

    tasks.append(task)
    save_tasks(tasks)
    print(f"Tarea agregada con ID {task['id']}")


def command_list(args):
    tasks = load_tasks()

    filtered = []
    for task in tasks:
        if args.pending and task["done"]:
            continue
        if args.done and not task["done"]:
            continue
        if args.priority and task["priority"] != args.priority:
            continue
        filtered.append(task)

    if not filtered:
        print("No hay tareas para mostrar")
        return

    for task in filtered:
        status = "x" if task["done"] else " "
        print(f"[{status}] {task['id']} - ({task['priority']}) {task['descripcion']}")


def command_done(args):
    tasks = load_tasks()
    task = find_task(tasks, args.id)

    if task is None:
        print(f"Error: no existe una tarea con ID {args.id}", file=sys.stderr)
        sys.exit(1)

    task["done"] = True
    save_tasks(tasks)
    print(f"Tarea {args.id} marcada como completada")


def command_remove(args):
    tasks = load_tasks()
    task = find_task(tasks, args.id)

    if task is None:
        print(f"Error: no existe una tarea con ID {args.id}", file=sys.stderr)
        sys.exit(1)

    answer = input(f"Eliminar tarea {args.id}: '{task['descripcion']}'? [s/N]: ").strip().lower()
    if answer not in {"s", "si", "y", "yes"}:
        print("Eliminacion cancelada")
        return

    updated = [item for item in tasks if item["id"] != args.id]
    save_tasks(updated)
    print(f"Tarea {args.id} eliminada")


def main():
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "add":
        command_add(args)
    elif args.command == "list":
        command_list(args)
    elif args.command == "done":
        command_done(args)
    elif args.command == "remove":
        command_remove(args)


if __name__ == "__main__":
    main()
