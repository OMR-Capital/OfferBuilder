/* eslint-disable @typescript-eslint/no-unused-vars */
import type { Writable } from "svelte/store";
import { writable } from "svelte/store";
import type { User } from "./backend/models/users";


export const user: Writable<User> = writable();
