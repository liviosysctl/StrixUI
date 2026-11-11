// The bundle is plain CSS classes (prefix k-) plus a small script, window.Kit. No framework.
// Markup for every component is in its README and preview.

export interface SegmentedHandle { select(index: number, silent?: boolean): void; place(): void; readonly index: number }
export interface CarouselHandle { select(index: number, silent?: boolean): void; readonly index: number }
export interface DockHandle { open(button: HTMLElement): void; close(): void; show(): void; hide(): void }
export interface VisualizerHandle { frame(levels?: number[]): void; start(): void; stop(): void }

export interface KitApi {
  /** Wires every component inside root: icons, wallpaper, segmented, sliders, rings, rolling numbers, calendars, visualizers, carousels, docks. Safe to call again. */
  hydrate(root?: ParentNode): void;
  /** Names of the bundled symbols. */
  icons: string[];
  /** SVG markup for one symbol (24px grid, 1.5 stroke, currentColor). */
  icon(name: string): string;
  /** SVG markup of the default wallpaper, drawn with the theme's tokens. */
  wallpaper(): string;
  /** True when motion should be reduced (system setting, or data-motion="reduced" on the html element). */
  reduced(): boolean;
  segmented(el: HTMLElement): SegmentedHandle;
  slider(input: HTMLInputElement): void;
  ring(el: HTMLElement, value?: number): void;
  roll(el: HTMLElement, text?: string): void;
  calendar(el: HTMLElement, date?: Date): void;
  visualizer(el: HTMLElement): VisualizerHandle;
  carousel(el: HTMLElement): CarouselHandle;
  dock(el: HTMLElement): DockHandle;
  /** Circular reveal of layer from a viewport point; resolves when it covers the layer. */
  reveal(layer: HTMLElement, x: number, y: number): Promise<void>;
  /** Plays the exit animation, then removes the element. */
  dismiss(el: HTMLElement, className?: string): void;
}
declare global { interface Window { Kit: KitApi } }
