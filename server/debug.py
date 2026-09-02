from models.ActionPayload import ActionPayload, Action, ActionType
from services.action_services import (
    filterResolvedActions,
    SaveNewLogs,
    getequivalentActionsList,
    resolveActions
)


def choose_action():
    print("\nAction types:")
    print("1. CREATE")
    print("2. MODIFY")
    print("3. DELETE")
    print("4. MOVE")

    while True:
        choice = input("Choose action: ")

        if choice == "1":
            return ActionType.CREATE

        if choice == "2":
            return ActionType.MODIFY

        if choice == "3":
            return ActionType.DELETE

        if choice == "4":
            return ActionType.MOVE

        print("Invalid choice.")


def create_action(action_id):
    print(f"\n========== ACTION {action_id} ==========")

    path = input("Path: ")

    action_type = choose_action()

    user = input("User: ")

    action_time = input("Time: ")

    old_path = None

    if action_type == ActionType.MOVE:
        old_path = input("Old path: ")

    return Action(
        id=action_id,
        path=path,
        action=action_type,
        user=user,
        time=action_time,
        oldPath=old_path
    )


def print_actions(actions, title):
    print(f"\n========== {title} ==========")

    if not actions:
        print("No actions.")
        return

    for action in actions:
        print(
            f"ID={action.id} | "
            f"path={action.path} | "
            f"action={action.action.value} | "
            f"user={action.user} | "
            f"time={action.time} | "
            f"oldPath={action.oldPath}"
        )


def main():

    print("========================================")
    print("       ACTION SERVICES TEST")
    print("========================================")

    agent_id = int(input("Agent ID: "))
    host_name = input("Hostname: ")

    number_of_actions = int(
        input("Number of actions: ")
    )

    actions = []

    for i in range(1, number_of_actions + 1):
        actions.append(create_action(i))

    payload = ActionPayload(
        agent_id=agent_id,
        hostName=host_name,
        actions=actions
    )

    print_actions(
        payload.actions,
        "ORIGINAL ACTIONS"
    )

    # --------------------------------------------------
    # Filter already resolved actions
    # --------------------------------------------------

    actions = filterResolvedActions(payload)

    print_actions(
        actions,
        "AFTER FILTERING RESOLVED ACTIONS"
    )

    if not actions:
        print("\nThere are no new actions to process.")
        return

    # --------------------------------------------------
    # Save new logs
    # --------------------------------------------------

    print("\n========== SAVING LOGS ==========")

    SaveNewLogs(actions)

    # --------------------------------------------------
    # Device folder
    # --------------------------------------------------

    device_folder = str(agent_id)

    print("\nDevice folder:", device_folder)

    # --------------------------------------------------
    # Equivalent actions
    # --------------------------------------------------

    equivalent_actions = getequivalentActionsList(
        actions,
        device_folder
    )

    print("\n========== EQUIVALENT ACTIONS ==========")

    if not equivalent_actions:
        print("No equivalent actions.")
    else:
        for path, action in equivalent_actions.items():
            print(
                f"path={path} | "
                f"equivalent action={action}"
            )

    # --------------------------------------------------
    # Resolve actions
    # --------------------------------------------------

    files_to_upload = resolveActions(
        equivalent_actions,
        device_folder
    )

    print("\n========== FILES TO UPLOAD ==========")

    if not files_to_upload:
        print("No files to upload.")
    else:
        for path in files_to_upload:
            print(path)

    print("\n========================================")
    print("TEST COMPLETE")
    print("========================================")


if __name__ == "__main__":
    main()