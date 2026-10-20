---
name: ros2-debugging
description: "Diagnose ROS 2 systems: nodes that never connect, topics with no data or the wrong rate, QoS mismatches, launch and parameter problems, and build failures with colcon. Use when a ROS 2 graph misbehaves or when you need to explain why a node, topic, or service is silent."
---

# ROS 2 Debugging

Work from the graph outward: confirm the middleware and discovery layer first, then topics and QoS, then the node's own logic. Most "the node does nothing" reports are one of four things: a different `ROS_DOMAIN_ID`, a QoS mismatch, a wrong topic name or namespace, or a node that never started.

## Step 1: Confirm the environment

Run these before touching code:

```bash
printenv | grep -E '^(ROS_|RMW_)'     # ROS distro, domain id, RMW implementation
ros2 doctor --report                   # network, middleware, and package health
ros2 node list                         # nodes visible from this shell
```

- Different `ROS_DOMAIN_ID` values in two terminals make nodes invisible to each other. This is the most common cause of "nothing shows up".
- `ROS_LOCALHOST_ONLY=1` or a restrictive firewall stops discovery across machines.
- Sourcing the wrong overlay (`install/setup.bash` from another workspace) runs a different version of a package than you edited.

## Step 2: Check the topic graph

```bash
ros2 topic list -t                     # topics and types
ros2 topic info -v /topic_name         # publishers, subscribers, and their QoS
ros2 topic hz /topic_name              # actual publish rate
ros2 topic echo /topic_name --once     # one message, to check content and frame_id
```

Rules of thumb:

- A topic that appears in `topic list` with no publisher was advertised by a node that has since died. Check `ros2 node info <node>`.
- A message type mismatch (for example one node built against a different version of a custom message package) means the subscriber never receives data. Compare `ros2 topic info -v` type on both ends and rebuild the message package.
- Remapping hides the real name. Check `ros2 node info` and the launch file before assuming the topic name in the code is the one on the wire.

## Step 3: Diagnose QoS mismatches

A publisher and subscriber only connect when their QoS is compatible. The usual failure is a `BEST_EFFORT` publisher (for example a camera driver) with a `RELIABLE` subscriber, which receives nothing and logs a warning at most.

```bash
ros2 topic info -v /camera/image_raw   # compare the Reliability and Durability columns
```

Fix on the side that is wrong for its data:

- Sensor streams: publisher and subscriber both `BEST_EFFORT`, with a small depth.
- Latched configuration: `TRANSIENT_LOCAL` on the publisher so late subscribers still get the last message.
- Do not change QoS on both sides to "make it work" without understanding why the data is lossy or delayed.

## Step 4: Logs, parameters, and timing

```bash
ros2 run <pkg> <node> --ros-args --log-level debug
ros2 param list /node_name
ros2 param get /node_name some_param
ros2 param dump /node_name             # what the node is really running with
ros2 bag record -a -o run_$(date +%s)  # capture everything for offline replay
ros2 bag play run_xxx --clock          # replay with simulated time
```

- For timing problems, record a bag and replay it rather than debugging on live hardware.
- Use `use_sim_time` consistently. A node on wall time next to a node on bag time looks like a timestamp failure.

## Step 5: Launch and build failures

```bash
colcon build --symlink-install --packages-up-to <pkg>
colcon test --packages-select <pkg> && colcon test-result --verbose
```

- `Package not found` after a successful build usually means the overlay was not sourced in the current shell.
- If a launch file starts nodes you did not expect, print the resolved configuration with `ros2 launch <pkg> <file.launch.py> --show-args` and read the included files.
- Stale build artefacts cause phantom errors. Remove only the affected package's `build/<pkg>` and `install/<pkg>` directories, not the whole workspace.

## Step 6: Reproduce in isolation

Before fixing node logic, reduce the system:

1. Run the failing node alone with recorded or synthetic input.
2. Add the next node back and check the topic at each boundary.
3. Write the minimum reproduction as a test (`launch_testing` or a `pytest` node test) so the fix stays fixed.

## Reporting

When you finish, state the root cause in one line (for example: "publisher BEST_EFFORT, subscriber RELIABLE, no messages delivered"), the command that proved it, and the change that fixed it. Say explicitly if you could not reproduce it on live hardware.
