/**
 * Mobile language/theme menus.
 *
 * Starlight uses a native <select> inside a position:fixed + overflow:auto drawer.
 * On iOS/Android that picker is often clipped or never opens; on a narrow desktop
 * window it drops below the viewport. Replace the tap target with a fixed listbox.
 */
(() => {
	const HOSTS = '.mobile-preferences starlight-theme-select, .mobile-preferences starlight-lang-select';
	const MENU_ID = 'cp-select-menu';
	const BACKDROP_ID = 'cp-select-backdrop';

	/** @type {HTMLElement | null} */
	let openSelect = null;

	function closeMenu() {
		document.getElementById(MENU_ID)?.remove();
		document.getElementById(BACKDROP_ID)?.remove();
		document.querySelectorAll('.cp-select-overlay[aria-expanded="true"]').forEach((btn) => {
			btn.setAttribute('aria-expanded', 'false');
		});
		openSelect = null;
	}

	/**
	 * @param {HTMLSelectElement} select
	 * @param {HTMLElement} anchor
	 * @param {HTMLElement} overlay
	 */
	function openMenu(select, anchor, overlay) {
		closeMenu();
		openSelect = select;
		overlay.setAttribute('aria-expanded', 'true');

		const backdrop = document.createElement('div');
		backdrop.id = BACKDROP_ID;
		backdrop.className = 'cp-select-backdrop';
		backdrop.addEventListener('click', closeMenu);

		const menu = document.createElement('div');
		menu.id = MENU_ID;
		menu.className = 'cp-select-menu';
		menu.setAttribute('role', 'listbox');
		const label = overlay.getAttribute('aria-label');
		if (label) menu.setAttribute('aria-label', label);

		for (const option of Array.from(select.options)) {
			const item = document.createElement('button');
			item.type = 'button';
			item.setAttribute('role', 'option');
			item.setAttribute('aria-selected', option.selected ? 'true' : 'false');
			item.dataset.value = option.value;
			item.textContent = option.textContent ?? option.value;
			if (option.selected) item.classList.add('is-selected');
			item.addEventListener('click', () => {
				if (select.value !== option.value) {
					select.value = option.value;
					select.dispatchEvent(new Event('change', { bubbles: true }));
				}
				closeMenu();
			});
			menu.appendChild(item);
		}

		document.body.append(backdrop, menu);

		const rect = anchor.getBoundingClientRect();
		const menuRect = menu.getBoundingClientRect();
		const gap = 6;
		const margin = 8;
		const spaceBelow = window.innerHeight - rect.bottom - margin;
		const spaceAbove = rect.top - margin;
		const openUp = spaceBelow < menuRect.height && spaceAbove > spaceBelow;

		let left = rect.left;
		if (left + menuRect.width > window.innerWidth - margin) {
			left = Math.max(margin, window.innerWidth - menuRect.width - margin);
		}
		menu.style.left = `${Math.round(left)}px`;
		menu.style.minWidth = `${Math.round(Math.max(rect.width, 10.5 * 16))}px`;

		if (openUp) {
			const bottom = window.innerHeight - rect.top + gap;
			menu.style.bottom = `${Math.round(bottom)}px`;
			menu.style.top = 'auto';
			menu.style.maxHeight = `${Math.round(Math.max(spaceAbove, 8 * 16))}px`;
		} else {
			menu.style.top = `${Math.round(rect.bottom + gap)}px`;
			menu.style.bottom = 'auto';
			menu.style.maxHeight = `${Math.round(Math.max(spaceBelow, 8 * 16))}px`;
		}

		menu.querySelector('.is-selected')?.focus();
	}

	/**
	 * @param {HTMLElement} host
	 */
	function enhance(host) {
		if (host.querySelector('.cp-select-overlay')) return;
		const select = host.querySelector('select');
		const label = host.querySelector('label');
		if (!(select instanceof HTMLSelectElement) || !(label instanceof HTMLElement)) return;

		label.style.position = 'relative';
		select.setAttribute('tabindex', '-1');

		const overlay = document.createElement('button');
		overlay.type = 'button';
		overlay.className = 'cp-select-overlay';
		overlay.setAttribute('aria-haspopup', 'listbox');
		overlay.setAttribute('aria-expanded', 'false');
		const sr = label.querySelector('.sr-only');
		overlay.setAttribute(
			'aria-label',
			(sr?.textContent || select.getAttribute('aria-label') || '').trim()
		);
		overlay.addEventListener('click', (event) => {
			event.preventDefault();
			event.stopPropagation();
			if (overlay.getAttribute('aria-expanded') === 'true') closeMenu();
			else openMenu(select, label, overlay);
		});
		label.appendChild(overlay);
	}

	function enhanceAll() {
		document.querySelectorAll(HOSTS).forEach((host) => {
			if (host instanceof HTMLElement) enhance(host);
		});
	}

	document.addEventListener('keydown', (event) => {
		if (event.key === 'Escape' && openSelect) {
			event.preventDefault();
			closeMenu();
		}
	});
	window.addEventListener('resize', closeMenu);
	document.addEventListener(
		'scroll',
		(event) => {
			const menu = document.getElementById(MENU_ID);
			if (menu && event.target instanceof Node && menu.contains(event.target)) return;
			if (openSelect) closeMenu();
		},
		true
	);

	if (document.readyState === 'loading') {
		document.addEventListener('DOMContentLoaded', enhanceAll);
	} else {
		enhanceAll();
	}
})();
