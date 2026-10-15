export type Role = 'primary'|'secondary'|'stabilizer';
export interface AnatomicalMuscle {id:string;name:string;english:string;group:string;region:string;layer:'superficial'|'deep';}
export interface Exercise {id:string;name:string;english:string;equipment:string;relations:{muscleId:string;role:Role}[];instructions:string[];errors:string[];animation:string;source:string;}
export interface MuscleGroup {id:string;name:string;}
export interface MuscleRegion {id:string;name:string;}
export interface WorkoutTemplate {id:string;name:string;exerciseIds:string[];}
export interface PlannedWorkout {id:string;date:string;exerciseIds:string[];calendarEventId?:string;startTime?:string;endTime?:string;syncStatus:'local'|'synced'|'conflict';}
export interface CompletedSet {id:string;exerciseId:string;weight:number;reps:number;rir:number;}
export interface WorkoutSession {id:string;date:string;sets:CompletedSet[];notes:string;plannedWorkoutId?:string;}
